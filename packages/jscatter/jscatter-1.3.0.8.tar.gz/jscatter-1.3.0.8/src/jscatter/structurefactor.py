# -*- coding: utf-8 -*-
# written by Ralf Biehl at the Forschungszentrum Jülich ,
# Jülich Center for Neutron Science 1 and Institute of Complex Systems 1
#    Jscatter is a program to read, analyse and plot data
#    Copyright (C) 2015-2019  Ralf Biehl
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Fluid like and crystal like structure factors (sf) and directly related functions for scattering
related to interaction potentials between particles.

Fluid like include hard core SF or charged sphere sf and more.
For RMSA an improved algorithm is used based on the original idea (see Notes in RMSA).

For lattices of ordered mesoscopic materials (see :ref:`Lattice`) the analytic sf can be calculated in
powder average or as oriented lattice with domain rotation.

Additional the structure factor of atomic lattices can be calculated using atomic scattering length.
Using coordinates from CIF (Crystallographic Information Format) file allow calculation of atomic crystal lattices.


"""
import sys
import os
import numbers
import inspect
import math

import numpy as np
from numpy import linalg as la
import scipy
import scipy.integrate
import scipy.fft
import scipy.constants as constants
import scipy.special as special

from .dataarray import dataArray as dA
from .dataarray import dataList as dL
from . import parallel
from .graceplot import GracePlot as grace
from . import formel
from . import formfactor as ff
from .lattice import lattice, rhombicLattice, bravaisLattice, scLattice, bccLattice, \
    fccLattice, diamondLattice, hexLattice, hcpLattice, pseudoRandomLattice, sqLattice, \
    hex2DLattice, lamLattice, randomLattice, honeycombLattice
from .lattice import latticeFromCIF, latticeVectorsFromLatticeConstants

from  .libs import Two_Yukawa

try:
    from . import fscatter

    useFortran = True
except ImportError:
    useFortran = False

_path_ = os.path.realpath(os.path.dirname(__file__))

# variable to allow printout for debugging as if debug:print 'message'
# set it to integer value above debuglevel
debug = False


def _sqcoefOriginalHP(ir, eta, gek, ak, a=0., b=0., c=0., f=0., u=0., v=0., gamk=0., seta=0., sgek=0., sak=0., scal=0.,
                      g1=0.):
    """
    CALCULATES RESCALED VOLUME FRACTION AND CORRESPONDING COEFFICIENTS
    This is only for documenting the difference to the old algorithm.

    This is the iterative part to find rescaling parameter to get G(1+)>0 (Gillian condition) if G(1+)>0

    Returns:
    ir,eta,gek,ak,a,b,c,f,u,v,gamk,seta,sgek,sak,scal,g1

    seta IS THE RESCALED VOLUME FRACTION.
    sgek IS THE RESCALED CONTACT POTENTIAL.
    sak IS THE RESCALED SCREENING CONSTANT.
    a,b,c,f,u,v ARE THE MSA COEFFICIENTS.
    g1=G(1+) IS THE CONTACT VALUE OF G(R/SIG);
    FOR THE GILLAN CONDITION, THE DIFFERENCE FROM
    ZERO INDICATES THE COMPUTATIONAL ACCURACY.

    IR > 0: NORMAL EXIT, IR IS THE NUMBER OF ITERATIONS.
    < 0: FAILED TO CONVERGE.

    This is equivalent to the original HP Fortran code.
    The different conditions might have saved computing time in 1981.
    For some parameter conditions the rescaling is needed but not done.

    Also for some parameter contributions the wrong root for Fwww is used.

    """
    # set to zero to get debug messages; debuglevel>10 no messages
    debuglevel = 1
    itm = 40  # original 40
    acc = 5.e-6
    if debug > debuglevel: print('-- ')
    if ak >= (1 + 8. * eta):
        # for large screening (scl is small and ak is large)
        # ix=1  SOLVE FOR LARGE K, RETURN G(1+)
        ix, ir, g1, eta, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
            _sqfun(1, ir, g1, eta, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1, useHP=True)
        if debug > debuglevel: print('large screening ', ir, g1, ak, gamk, 'abcfuv', a, b, c, f, u, v)
        if ir < 0 or g1 >= 0:  # error or already a good solution is returned
            return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
        else:
            # we have to rescale the solution in the later as here g+<0
            pass
    seta = min(eta, 0.2)
    if ak >= (1 + 8. * eta) or gamk >= 0.15:
        # find a rescaled eta with g+>=0 for strong coupling or low volume fraction
        j = 0.
        f1 = 0.
        f2 = 0.
        while True:  # loop for Newton iteration to find g+=0
            j += 1
            if j > itm:
                return -1, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
            if seta <= 0.0: seta = eta / j  # g+<0 -> rescale eta
            if seta > 0.6: seta = 0.35 / j  # rescaled eta>0.6 rescale to smaller value
            e1 = seta  # e1 first eta
            # ix=2  RETURN FUNCTION TO SOLVE FOR ETA(GILLAN)
            ix, ir, f1, e1, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
                _sqfun(2, ir, f1, e1, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1, useHP=True)
            e2 = seta * 1.01  # increase scaled eta
            ix, ir, f2, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
                _sqfun(2, ir, f2, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1, useHP=True)
            e2 = e1 - (e2 - e1) * f1 / (f2 - f1)  # new approximation for scaled eta
            seta = e2  # save for next iteration or as result
            delta = abs((e2 - e1) / e1)  # relative change
            if delta < acc: break  # if changes are small enough then break
        if debug > debuglevel: print('rescaling with %i iterations leads to scaling by %.3g' % (j, seta / eta))
        # ix=4    RETURN G(1+) FOR ETA=ETA(GILLAN).
        ix, ir, g1, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g11 = \
            _sqfun(4, ir, g1, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1, useHP=True)
        ir = j
        # ---------------end of Newton loop
        if debug > debuglevel: print('rescaled ', ir, g1, ak, gamk, 'abcfuv', a, b, c, f, u, v, 'ak>,seta>eta ',
                                     ak >= (1 + 8. * eta), seta >= eta)
        if ak >= (1 + 8. * eta):  # in this case return anyway
            return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
        else:
            if seta >= eta:  # seta>eta indicates successful rescaling with g1 as zero
                return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1

    ix, ir, g1, eta, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
        _sqfun(3, ir, g1, eta, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1, useHP=True)
    if debug > debuglevel: print('after scaling ', ir, g1, ak, gamk, 'abcfuv', a, b, c, f, u, v)
    if ir >= 0:
        if g1 < 0.: ir = -3  # rescaling not successful
    return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1


def _sqcoef(ir, eta, gek, ak, a=0., b=0., c=0., f=0., u=0., v=0., gamk=0., seta=0., sgek=0., sak=0., scal=0., g1=0.):
    """
    CALCULATES RESCALED VOLUME FRACTION AND CORRESPONDING COEFFICIENTS

    This is the iterative part to find rescaling parameter to get G(1+)>0 (Gillian condition) if G(1+)>0

    Returns:
    ir,eta,gek,ak,a,b,c,f,u,v,gamk,seta,sgek,sak,scal,g1

    seta IS THE RESCALED VOLUME FRACTION.
    sgek IS THE RESCALED CONTACT POTENTIAL.
    sak IS THE RESCALED SCREENING CONSTANT.
    a,b,c,f,u,v ARE THE MSA COEFFICIENTS.
    g1=G(1+) IS THE CONTACT VALUE OF G(R/SIG);
    FOR THE GILLAN CONDITION, THE DIFFERENCE FROM
    ZERO INDICATES THE COMPUTATIONAL ACCURACY.

    IR > 0: NORMAL EXIT, IR IS THE NUMBER OF ITERATIONS.
    < 0: FAILED TO CONVERGE.

    This is a shorter version of sqcoef which is easier to understand and allows
    no bypassing between the conditions in original code which leads to errors for harmless parameter settings.
    The idea is the original idea (see [2]_) to calculate the MSA and to rescale if  g+<0  .


    """
    # set to zero to get debug messages; debuglevel>10 no messages
    debuglevel = 1
    itm = 80  # original 40
    acc = 5.e-6
    fix = 0.5
    if debug > debuglevel: print('-- ')
    # just try to solve
    ix, ir, g1, eta, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
        _sqfun(1, ir, g1, eta, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1)
    if debug > debuglevel: print('first try ', ir, g1, ak, gamk, 'abcfuv', a, b, c, f, u, v)
    if ir == -2:
        # FAILED TO CONVERGE in Newton algorith to find zero, only in classical HP solution,
        return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
    elif ir == -4:
        # no root found in first try
        return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
    elif g1 < 0:
        # we have to rescale the solution in the later as here g+<0
        pass
    elif g1 >= 0:  # already a good solution is returned
        return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1

    seta = min(eta, 0.2)
    # find a rescaled eta with g+>=0 for strong coupling or low volume fraction
    j = 0.
    f1 = 0.
    f2 = 0.
    while True:  # loop for Newton iteration to find g+=0
        j += 1
        if j > itm:
            return -1, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
        if seta <= 0.0: seta = eta / j  # g+<0 -> rescale eta
        if seta > 0.6: seta = 0.35 / j  # rescaled eta>0.6 rescale to smaller value
        e1 = seta  # e1 first eta
        # ix=2  RETURN FUNCTION TO SOLVE FOR ETA(GILLAN)
        ix, ir, f1, e1, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
            _sqfun(2, ir, f1, e1, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1)
        e2 = seta * 1.01  # increase scaled eta
        ix, ir, f2, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = \
            _sqfun(2, ir, f2, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1)
        e2 = e1 - (e2 - e1) * f1 / (f2 - f1)  # new approximation for scaled eta
        seta = e2  # save for next iteration or as result
        delta = abs((e2 - e1) / e1)  # relative change
        if delta < acc: break  # changes  are small enough then break
    if debug > debuglevel: print('rescaling with %i iterations leads to scaling by %.3g' % (j, seta / eta))
    # ix=4    RETURN G(1+) FOR ETA=ETA(GILLAN) with all parameters.
    ix, ir, g1, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g11 = \
        _sqfun(4, ir, g1, e2, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1)
    if (seta > 0.64) or (seta < eta):
        ir = -3  # rescaling not successful
        return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
    ir = j
    # ---------------end of Newton loop
    if debug > debuglevel: print('rescaled ', ir, g1, ak, gamk, 'abcfuv', a, b, c, f, u, v, 'ak>,seta,eta ',
                                 ak >= (fix + 8. * eta), seta, eta)
    return ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1


def _sqfun(ix, ir, fval, evar, reta, rgek, rak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1, useHP=False):
    """
    CALCULATES VARIOUS COEFFICIENTS AND FUNCTION VALUES FOR _sqcoef

    this is the NOT rescaled solution! == MSA

    Options
    ix =1: SOLVE FOR LARGE K, RETURN G(1+).
        2: RETURN FUNCTION TO SOLVE FOR ETA(GILLAN).
        3: ASSUME NEAR GILLAN, SOLVE, RETURN G(1+).
        4: RETURN G(1+) FOR ETA=ETA(GILLAN).

    SETA IS THE RESCALED VOLUME FRACTION.
    SGEK IS THE RESCALED CONTACT POTENTIAL.
    SAK IS THE RESCALED SCREENING CONSTANT.
    A,B,C,F,U,V ARE THE MSA COEFFICIENTS.
    G1=G(1+) IS THE CONTACT VALUE OF G(R/SIG);
    FOR THE GILLAN CONDITION, THE DIFFERENCE FROM
    ZERO INDICATES THE COMPUTATIONAL ACCURACY.

    IR > 0: NORMAL EXIT, IR IS THE NUMBER OF ITERATIONS.
     < 0: FAILED TO CONVERGE.

    The root of the quartic F = w4*fa**4+w3*fa**3+w2*fa**2+w1*fa+w0 needs to be found.
    in this code we have two choices in the source code.
    One for documentation and the second as the correct solution:

     1. to use the original HayterPenfold algorithm from the Fortran code as also eg used in SASVIEW and SASFIT
        with an estimate for the root of Fwww which is refined by Newton algorithm
        which results under specific conditions in the wrong root
        test with e.g.
        for scl in np.r_[1:10]:p.plot(js.sf.RMSA(q=x,R=3.1,scl=scl, gamma=1.1, eta=0.5),legend='%.3g' %scl)
        the correct branch can be verified by using the Percus-Yevick as limit

     2. original idea from Hayter paper [1]_ as *default  solution*
        find all roots (by numpy.roots) and take the physical root with g(r/diameter<1)=0
        in this code there is no difference between ix=1 and 3
        with structurefactor.debug=11 you get output for g(r) and the zeros of Fwww (see source code)



    """
    # set to zero to get debug messages; debuglevel>10 no messages
    debuglevel = 1
    acc = 1e-6  # stop criterion for Newton
    itm = 40  # max number of iterations
    # needed parameters with changes for iteration
    eta = evar  # volume fraction
    scal = (reta / evar) ** (1 / 3.)  # scaling factor
    sak = rak / scal  # scaled dimensionless screening constant
    val = rgek if abs(rgek) > 1e-9 else 1e-9  # prevent zero and just take small value
    sgek = val * scal * math.exp(rak - sak)  # scaled contact potential
    gek = sgek
    ak = sak
    # -----------------reproduce original fortran code
    # using these variables is important to reduce the dependency on accuracy of float64
    # and maybe it makes it a bit faster
    eta2 = eta ** 2
    eta3 = eta2 * eta
    e12 = 12. * eta
    e24 = e12 + e12
    ak2 = ak ** 2
    ak1 = 1 + ak
    dak2 = 1.0 / ak2
    dak4 = dak2 * dak2
    d = 1 - eta
    d2 = d * d
    dak = d / ak
    dd2 = 1.0 / d2
    dd4 = dd2 * dd2
    dd45 = dd4 * 2.0e-1
    eta3d = 3. * eta
    eta6d = eta3d + eta3d
    eta32 = eta3 + eta3
    eta2d = eta + 2.0
    eta2d2 = eta2d * eta2d
    eta21 = 2.0 * eta + 1.0
    eta22 = eta21 * eta21

    # all coefficients from appendix in the paper [1]
    al1 = -eta21 * dak
    al2 = (14 * eta2 - 4 * eta - 1) * dak2
    al3 = 36 * eta2 * dak4

    b1 = -(eta2 + 7. * eta + 1.) * dak
    b2 = 9. * eta * (eta2 + 4. * eta - 2.) * dak2
    b3 = 12. * eta * (2 * eta2 + 8. * eta - 1.) * dak4

    n1 = -(eta3 + 3. * eta2 + 45. * eta + 5.) * dak
    n2 = (eta32 + 3. * eta2 + 42. * eta - 20.) * dak2
    n3 = (eta32 + 30. * eta - 5.) * dak4
    n4 = n1 + 24. * eta * ak * n3
    n5 = eta6d * (n2 + 4. * n3)

    f1 = eta6d / ak
    f2 = d - 12. * eta * dak2

    ff1 = f1 * f1
    ff2 = f2 * f2
    ff = ff1 + ff2
    f1f2 = 2. * f1 * f2

    t1 = (eta + 5.) / (5. * ak)
    t2 = eta2d * dak2
    t3 = -12. * eta * gek * (t1 + t2)
    t4 = eta3d * ak2 * (t1 * t1 - t2 * t2)
    t5 = eta3d * (eta + 8.) * 0.1 - 2. * eta22 * dak2
    # ------------
    a1 = (e24 * gek * (al1 + al2 + ak1 * al3) - eta22) * dd4
    bb1 = (1.5 * eta * eta2d2 - 12. * eta * gek * (b1 + b2 + ak1 * b3)) * dd4
    v1 = (eta21 * (eta2 - 2. * eta + 10.) * 0.25 - gek * (n4 + n5)) * dd45
    p1 = (gek * (ff1 + ff2 - f1f2) - 0.5 * eta2d) * dd2
    T1 = t3 + t4 * a1 + t5 * bb1

    if (sak > 15) and (ix == 1):
        if debug > debuglevel: print('(sak>15) and (ix==1)', ak)
        # this corresponds to ibig=1 in original Hayter-Penfold code for large screening
        # large screening means the screening length 1/kappa is small compared to 2R and we are in the hard sphere limit
        # if ak is big -> cosh = sinh and a lot simplifies in asymptotic solution
        # but at same time cosh(ak) may exceeds numerical limits for really large ak
        a3 = e24 * (eta22 * dak2 - 0.5 * d2 - al3) * dd4
        bb3 = e12 * (0.5 * d2 * eta2d - eta3d * eta2d2 * dak2 + b3) * dd4
        v3 = ((eta3 - 6. * eta2 + 5.) * d - eta6d * (2. * eta3 - 3. * eta2 + 18. * eta + 10.) * dak2 + e24 * n3) * dd45
        p3 = (ff1 - ff2) * dd2
        T3 = t4 * a3 + t5 * bb3 + e12 * t2 - 0.4 * eta * (eta + 10.) - 1.
        M6 = T3 * a3 - e12 * v3 * v3
        M5 = T1 * a3 + a1 * T3 - e24 * v1 * v3
        M4 = T1 * a1 - e12 * v1 * v1
        L6 = e12 * p3 * p3
        L5 = e24 * p1 * p3 - 2. * bb3 - ak2
        L4 = e12 * p1 * p1 - 2. * bb1
        W56 = M5 * L6 - L5 * L6
        W46 = M4 * L6 - L4 * M6
        fa = -W46 / W56
        ca = -fa
        f = fa
        c = ca
        b = bb1 + bb3 * fa
        a = a1 + a3 * fa
        v = v1 + v3 * fa
        g1 = -(p1 + p3 * fa)
        fval = g1 if g1 > 1e-3 else 0.
        seta = evar
        # g24 = e24*gek*math.exp(ak)            # prevent math range error in exp for large ak (-> small scl)
        # u = (ak2*ak*ca-g24)/(ak2*g24)         # so we rewrite this to have exp(-ak)
        u = ak * ca / e24 / gek * math.exp(-ak) - 1 / ak2  # same as above two lines but this prevents math range error
        return ix, ir, fval, evar, reta, rgek, rak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1

    # small sak for the remaining
    sk = math.sinh(ak)
    ck = math.cosh(ak)
    ckma = ck - 1. - ak * sk
    skma = sk - ak * ck
    a2 = e24 * (al3 * skma + al2 * sk - al1 * ck) * dd4
    a3 = e24 * (eta22 * dak2 - 0.5 * d2 + al3 * ckma - al1 * sk + al2 * ck) * dd4

    bb2 = e12 * (-b3 * skma - b2 * sk + b1 * ck) * dd4
    bb3 = e12 * (0.5 * d2 * eta2d - eta3d * eta2d2 * dak2 - b3 * ckma + b1 * sk - b2 * ck) * dd4

    v2 = (n4 * ck - n5 * sk) * dd45
    v3 = ((eta3 - 6. * eta2 + 5.) * d - eta6d * (
            2. * eta3 - 3. * eta2 + 18. * eta + 10.) * dak2 + e24 * n3 + n4 * sk - n5 * ck) * dd45
    # define...
    p2 = (ff * sk + f1f2 * ck) * dd2
    p3 = (ff * ck + f1f2 * sk + ff1 - ff2) * dd2

    T2 = t4 * a2 + t5 * bb2 + e12 * (t1 * ck - t2 * sk)
    T3 = t4 * a3 + t5 * bb3 + e12 * (t1 * sk - t2 * (ck - 1.)) - 0.4 * eta * (eta + 10.) - 1.

    M1 = T2 * a2 - e12 * v2 * v2
    M2 = T1 * a2 + T2 * a1 - e24 * v1 * v2
    M3 = T2 * a3 + T3 * a2 - e24 * v2 * v3
    M4 = T1 * a1 - e12 * v1 * v1
    M5 = T1 * a3 + T3 * a1 - e24 * v1 * v3
    M6 = T3 * a3 - e12 * v3 * v3

    # ix is defined from the _sqcoef
    #  large k or close to GILLAN CONDITION g1==0 as explained in [1]
    if ix == 1 or ix == 3:
        # YES - G(X=1+) = 0
        # COEFFICIENTS AND FUNCTION VALUE
        L1 = e12 * p2 * p2
        L2 = e24 * p1 * p2 - 2. * bb2
        L3 = e24 * p2 * p3
        L4 = e12 * p1 * p1 - 2. * bb1
        L5 = e24 * p1 * p3 - 2. * bb3 - ak2
        L6 = e12 * p3 * p3

        W16 = M1 * L6 - L1 * M6
        W15 = M1 * L5 - L1 * M5
        W14 = M1 * L4 - L1 * M4
        W13 = M1 * L3 - L1 * M3
        W12 = M1 * L2 - L1 * M2
        W26 = M2 * L6 - L2 * M6
        W25 = M2 * L5 - L2 * M5
        W24 = M2 * L4 - L2 * M4
        W36 = M3 * L6 - L3 * M6
        W35 = M3 * L5 - L3 * M5
        W34 = M3 * L4 - L3 * M4
        W32 = M3 * L2 - L3 * M2
        W46 = M4 * L6 - L4 * M6
        W56 = M5 * L6 - L5 * M6

        # QUARTIC COEFFICIENTS W(I)
        #  these are used in
        # fun = w0+(w1+(w2+(w3+w4*fa)*fa)*fa)*fa  =w4*fa**4+w3*fa**3+w2*fa**2+w1*fa+w0
        w4 = W16 * W16 - W13 * W36
        w3 = 2. * W16 * W15 - W13 * (W35 + W26) - W12 * W36
        w2 = W15 * W15 + 2. * W16 * W14 - W13 * (W34 + W25) - W12 * (W35 + W26)
        w1 = 2. * W15 * W14 - W13 * W24 - W12 * (W34 + W25)
        w0 = W14 * W14 - W12 * W24
        # now find root of fun
        if useHP:
            # this documents the original HayterPenfold algorithm as found in original fortran code
            # to find the correct root an estimate is used and refined by Newton method
            # fails eg for R=3.1 gam=1.1 eta=0.5 when scl 6.1999 -> 6,2 as sak changes over 1
            # or scl=1.37382379588 R=2.5 gam=5.1 eta=0.6 as the found root results in g(r<1)>0
            # reason: in Newton refining an arbitrary root is found
            if ix == 1:  # large screening
                # LARGE K estimate for the zero of Fwww
                fap = (W14 - W34 - W46) / (W12 - W15 + W35 - W26 + W56 - W32)
            else:  # ix=3  no large screening
                # ASSUME NOT TOO FAR FROM GILLAN CONDITION.
                # IF BOTH RGEK AND RAK ARE SMALL, USE P-W ESTIMATE.of the zero of Fwww
                g1 = 0.5 * eta2d * dd2 * math.exp(-gek)
                pg = p1 + g1
                ca = ak2 * pg + 2. * (bb3 * pg - bb1 * p3) + e12 * g1 * g1 * p3
                ca = -ca / (ak2 * p2 + 2. * (bb3 * p2 - bb2 * p3))
                fap2 = -(pg + p2 * ca) / p3
                if (gek > 0) and (sgek <= 2.0) and (sak <= 1.0):
                    # gek>0 as this is only for positive contact potentials
                    # this was introduced in the SASFIT conversion (C code)
                    e24g = e24 * gek * math.exp(ak)
                    pwk = math.sqrt(e24g)
                    qpw = (1. - math.sqrt(1. + 2. * d2 * d * pwk / eta22)) * eta21 / d
                    g1 = -qpw * qpw / e24 + 0.5 * eta2d * dd2
                pg = p1 + g1
                ca = ak2 * pg + 2. * (bb3 * pg - bb1 * p3) + e12 * g1 * g1 * p3
                ca = -ca / (ak2 * p2 + 2. * (bb3 * p2 - bb2 * p3))
                fap = -(pg + p2 * ca) / p3
                # print('PWEstimate',fap,fap2,( sgek<=2.0) and ( sak<=1.0))
            # now find a better estimate of the zero by Newton iteration
            # RB: this algorithm finds different roots dependent on sgek and sak
            # the roots are somehow arbitrary in the 4 possible ones,
            # the main time it is one of the two centered which make no
            # big jumps but the outer ones make large jumps in the result
            ii = 0
            while True:
                ii += 1
                if ii > itm:  # FAILED TO CONVERGE IN ITM ITERATIONS
                    ir = -2
                    return ix, ir, fval, evar, reta, rgek, rak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1
                fa = fap  # estimated zero pole of fun
                fun = w0 + (w1 + (w2 + (w3 + w4 * fa) * fa) * fa) * fa  # function to minimize
                fund = w1 + (2. * w2 + (3. * w3 + 4. * w4 * fa) * fa) * fa  # derivative of fun
                fap = fa - fun / fund  # new value as next estimate
                if fa == 0: continue  # fa is 0 if gek is zero
                delta = abs((fap - fa) / fa)  # difference
                if delta < acc: break
            # found one and use this zero
            ir = ir + ii
            fa = fap
            ca = -(W16 * fa * fa + W15 * fa + W14) / (W13 * fa + W12)
            g1 = -(p1 + p2 * ca + p3 * fa)
        else:
            # original idea from Hayter paper [1]_
            # take all roots and use the physical root with g(r/diameter<1)=0
            # in this code there is no difference between ix=1 or 3
            # The algorithm relies on computing the eigenvalues of the companion matrix
            x0 = np.roots(
                [w4, w3, w2, w1, w0])  # 114µs      slower than direct calculation, but this is not the bottle neck
            if np.all((x0.imag / x0.real) < 1e-3):
                # if the imaginary part of complex roots is small use also these
                # in some cases this is the correct solution in gr
                fa = x0.real
            else:
                fa = x0[np.isreal(x0)].real  # 6.5µs
            fa.sort()  # we have up to 4 real roots and each of the following has up to 4 values
            ca = -(W16 * fa * fa + W15 * fa + W14) / (W13 * fa + W12)
            g1 = -(p1 + p2 * ca + p3 * fa)
            b = bb1 + bb2 * ca + bb3 * fa
            a = a1 + a2 * ca + a3 * fa
            # choose the correct root by calculating g(r) (sin transform) and using the one with g(r<1)=0
            # here i choose explicitly 1-delta
            delta = 0.05
            nn = (2 ** 13 + 0)  # n number of points to get reliable fft
            dqr2 = np.r_[0, delta:nn * delta:delta]  # points to calculate S(dqr2)
            kk = 1 // delta  # index of last point smaller 1
            # calc the value of g(x) with x=1-delta=kk*delta  in equ.12 of[1]_
            gr1 = [delta * np.sum(
                (_SQMSA(dqr2, scal, eta, ak, gek, aa, bb, cca, ffa) - 1) * dqr2 * np.sin(kk * delta * dqr2))
                   for aa, bb, cca, ffa in zip(a, b, ca, fa)]
            grval = [1 + ggr / (12 * np.pi * eta * kk * delta) for ggr in gr1]
            if len(fa) == 0 or np.min(grval) > 0.1:
                # no real root found or not grval close to zero
                ir = -4
                return ix, ir, fval, evar, reta, rgek, rak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, \
                       g1.max() if np.size(g1) else g1
            # chose the one with grval close to zero
            chooseone = np.argmin(np.abs(grval))
            if debug > debuglevel:
                # this writes the calculated g(r) to a file for checking of g(r)
                rrr = 2 * np.pi * np.fft.rfftfreq(len(dqr2), d=delta)  # points in r domain from rfft r/diameter
                # doing sin transform with rfft results in minus in front of imag part
                # compared to equation 12 in HP paper [1]
                # delta* is to get correct integral
                # gr=[delta*np.fft.rfft((_SQMSA(dqr2,scal,eta,ak,gek,aa,bb,cca,ffa)-1)*dqr2).imag
                #                                            for aa,bb,cca,ffa in zip(a,b,ca,fa)]
                gr = [delta * scipy.fft.dst(_SQMSA(dqr2, scal, eta, ak, gek, aa, bb, cca, ffa) - 1) * dqr2
                      for aa, bb, cca, ffa in zip(a, b, ca, fa)]
                # [1:] to avoid rrr=zero
                gr = [1 - ggr[1:] / (12 * np.pi * eta * rrr[1:]) for ggr in gr]
                # choose one with minimum mean value g(r) for rrr<1 which should be zero
                # above we use only one value and choose smallest grval
                # here we choose the smallest mean value which is often not correct but here it is only for demo
                grval = [grr[rrr[1:] < 0.9][1:].mean() for grr in gr]
                print('grval  ', grval)
                temp = dL()
                for i, grr in enumerate(gr):
                    temp.append(np.c_[rrr[1:], grr].T)
                    temp[-1].choosen = chooseone
                    temp[-1].zero = fa[i]
                    temp[-1].g1 = g1[i]
                    temp[-1].legend = 'g(r<1)= %.3g' % (grval[i])
                temp.savetxt('testgr.dat')
                print('zeros,g1,choosen zero', fa, g1, chooseone)
            fa = fa[chooseone]
            ca = ca[chooseone]
            g1 = -(p1 + p2 * ca + p3 * fa)
            # end searching the root- recalculating final result------------------------
        fval = (g1 if abs(g1) > 1e-3 else 0.)
        seta = evar
        f = fa
        c = ca
        b = bb1 + bb2 * ca + bb3 * fa
        a = a1 + a2 * ca + a3 * fa
        v = (v1 + v2 * ca + v3 * fa) / a

    else:
        # -> ix==2 or ix==4
        ca = ak2 * p1 + 2. * (bb3 * p1 - bb1 * p3)
        ca = -ca / (ak2 * p2 + 2.0 * (bb3 * p2 - bb2 * p3))
        fa = -(p1 + p2 * ca) / p3
        # fval will contain g1 for Newton iteration ix=2,4
        if ix == 2:    fval = M1 * ca * ca + (M2 + M3 * fa) * ca + M4 + M5 * fa + M6 * fa * fa
        if ix == 4:    fval = -(p1 + p2 * ca + p3 * fa)
        f = fa
        c = ca
        b = bb1 + bb2 * ca + bb3 * fa
        a = a1 + a2 * ca + a3 * fa
        v = (v1 + v2 * ca + v3 * fa) / a
    g24 = e24 * gek * math.exp(ak)
    u = (ak2 * ak * ca - g24) / (ak2 * g24)
    return ix, ir, fval, evar, reta, rgek, rak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1


def _SQMSA(qR2, scal, eta, ak, gek, a, b, c, f):
    """
    equation 14 Hayter-Penfold paper [1] in sfRMSA to calculate the final structure factor
    """
    K = np.where(qR2 == 0, 1e-15, qR2 / scal)  # catch zero
    if ak > 25:  # c==-f and
        # avoid to large ak to prevent math range error
        # ak>15 has f=-c from sqfun so the sinh and cosh terms cancel for large ak
        sinhsk = 0.
        coshsk = 0.
    else:
        sinhsk = math.sinh(ak)
        coshsk = math.cosh(ak)
    sink = np.sin(K)
    cosk = np.cos(K)
    K2 = K * K
    K3 = K2 * K
    K4 = K3 * K
    KK2ak2 = 1 / K / (K2 + ak ** 2)
    a_K = a * (sink - K * cosk) / K3 \
          + b * ((2. / K ** 2 - 1) * K * cosk + 2 * sink - 2. / K) / K3 \
          + a * eta * (24. / K3 + 4. * (1 - 6. / K2) * sink - (1 - 12. / K2 + 24. / K4) * K * cosk) / 2. / K3 \
          + c * (ak * coshsk * sink - K * sinhsk * cosk) * KK2ak2 \
          + f * (ak * sinhsk * sink - K * (coshsk * cosk - 1)) * KK2ak2 \
          + f * (cosk - 1) / K2 \
          - gek * (ak * sink + K * cosk) * KK2ak2
    msa = 1 / (1 - 24. * eta * a_K)
    MSA = np.where(qR2 == 0, -1 / a, msa)  # -1/a is correct solution for qR2==zero
    return MSA


def RMSA(q, R, scl, gamma, molarity=None, eta=None, useHP=False):
    r"""
    Structure factor for a screened coulomb interaction (single Yukawa) in rescaled mean spherical approximation (RMSA).

    Structure factor according to Hayter-Penfold [1]_ [2]_ .
    Consider a scattering system consisting of macro ions, counter ions  and solvent.
    Here an improved algorithm [3]_ is used based on the original idea described in [1]_ (see Notes).

    Parameters
    ----------
    q : array; N dim
        Scattering vector; units 1/nm
    R : float
        Radius of the object; units nm
    molarity : float
        Number density n in units mol/l. Overrides eta, if both given.
    scl : float>0
        Screening length; units nm; negative values evaluate to scl=0.
    gamma : float
        Contact potential :math:`\gamma` in units kT.
         - :math:`\gamma=Z_m/(\pi \epsilon \epsilon_0 R (2+\kappa R))`
          - :math:`Z_m = Z^*` effective surface charge
          - :math:`\epsilon_0,\epsilon` free permittivity and dielectric constant
          - :math:`\kappa=1/scl` inverse screening length of Debye-Hückel potential
    eta : float
        Volume fraction as eta=:math:`4/3piR^3n`  with number density n.
    useHP : True, default False
        To use the original Hayter/Penfold algorithm. This gives wrong results for some parameter conditions.
        It should ONLY be used for testing.
        See example examples/test_newRMSAAlgorithm.py for a direct comparison.

    Returns
    -------
    dataArray
         - .volumeFraction = eta
         - .rescaledVolumeFraction
         - .screeningLength
         - .gamma=gamma
         - .contactpotential
         - .S0 structure factor at q=0
         - .scalingfactor factor for rescaling to get g+1=0; if =1 nothing was scaled and it is MSA

    Notes
    -----
    The repulsive potential between two identical spherical macroions of diameter :math:`\sigma` is (DLVO model)
    in dimensionless form

    .. math:: \frac{U(x)}{k_BT} = \gamma \frac{e^{-kx}}{x}   \; for \; x>1

    - :math:`x = r/\sigma, k=\kappa\sigma, K=Q\sigma`
    - :math:`k_BT` thermal energy
    - :math:`\gamma e^{-k} = \frac{\pi \epsilon_0 \epsilon \sigma }{k_BT} \psi^2_0` contact potential in kT units
    - The potential is completed by :math:`U(x)/kT=\infty , x<1`

    - From [1]_:
       This potential is valid for colloid systems provided k < 6.
       There is no theoretical restriction on k in what follows, however, and for general studies
       of one component plasmas any value may be used.
    - In the limit :math:`\gamma \rightarrow 0` or :math:`k\rightarrow\infty` the Percus-Yevick hard sphere is reached.
    - Why is is named **rescaled MSA**:
      From [1]_:
       Note that in general, however, the MSA fails at low density; letting :math:`n\rightarrow0` yields
       :math:`g(x)\rightarrow 1-lU(x)/kT` for x> 1. Since U(x) is generally larger than thermal energies
       for small interparticle separations, g(x) will generally be negative (and hence unphysical)
       near the particle at very low densities.
       This does not present a problem for many colloid studies of current interest, where volume fractions are
       generally greater than 1%.

      To solve this the radius is rescaled to get :math:`g(\sigma +)=0` according to [2]:
        ...by increasing the particle diameter from its physical value `a` to an effective hard core value `a'`,
        while maintaining the Coulomb coupling constant. ...

      If :math:`g(\sigma +)>=0` no rescaling is done.


    Improved algorithm (see [3]_ fig. 6)
     The Python code is deduced from the original Hayter-Penfold Fortran code (1981, ILL Grenoble).
     This is also used in other common SAS programs as SASfit or SASview (translated to C).
     The original algorithm determines the root of a quartic F(w1,w2,w3,w4) by an estimate (named PW estimate),
     refining it by a Newton algorithm. As the PW estimate is sometimes not good enough this results in an
     arbitrary root of the quartic in the Newton algorithm. The solution therefore jumps between different
     possibilities by small changes of the parameters.
     We use here the original idea from [1]_ to calculate G(r<0) for all four roots of F(w1,w2,w3,w4) and use
     the physical solution with G(r<R)=0.
     See examples/test_newRMSAAlgorithm.py for a direct comparison or [3]_ fig. 6.

    Validity
     The calculation of charge at the surface or screening length from a solute ion concentration is explicitly dedicate
     to the user. The Debye-Hückel theory for a macro ion in screened solution is a far field theory as a linearization
     of the Poisson-Boltzmann (PB) theory and from limited validity (far field or low charge -> linearization).
     Things like reverting charge layer, ion condensation at the surface, pH changes at the surface or other things
     might appear. Before calculating please take these things into account. Close to the surface the PB
     has to be solved. The DH theory can still be used if the charge is thus an effective charge named Z*,
     which might be different from the real surface charge.
     See Ref [4]_ for details.

    Examples
    --------
    Effekt of volume fraction, surfacepotential and screening length onto RMSA structure factor
    ::

     import jscatter as js
     R = 6
     eta0 = 0.2
     gamma0 = 30 # surface potential
     scl0 = 10
     q = js.loglist(0.01, 5, 200)
     p = js.grace(1,1.5)
     p.multi(3,1)
     for eta in [0.01,0.05,0.1,0.2,0.3,0.4]:
         rmsa = js.sf.RMSA(q, R, scl=scl0, gamma=gamma0, eta=eta)
         p[0].plot(rmsa, symbol=0, line=[1, 3, -1], legend=f'eta ={eta:.1f}')
     for scl in [0.1,1,5,10,20]:
         rmsa = js.sf.RMSA(q, R, scl=scl, gamma=gamma0, eta=eta0)
         p[1].plot(rmsa, symbol=0, line=[1, 3, -1], legend=f'scl ={scl:.1f}')
     for gamma in [1,10,20,40,100]:
         rmsa = js.sf.RMSA(q, R, scl=scl0, gamma=gamma, eta=eta0)
         p[2].plot(rmsa, symbol=0, line=[1, 3, -1], legend=r'\xG\f{} =$gamma')
     p[0].yaxis(min=0.0, max=2.5, label='S(Q)', charsize=1.5)
     p[0].legend(x=1.2, y=2.4)
     p[0].xaxis(min=0, max=1.5,label='')
     p[1].yaxis(min=0.0, max=2.2, label='S(Q)', charsize=1.5)
     p[1].legend(x=1.1, y=2.)
     p[1].xaxis(min=0, max=1.5, label=r'')
     p[2].yaxis(min=0.0, max=2.2, label='S(Q)', charsize=1.5)
     p[2].legend(x=1.1, y=2.2)
     p[2].xaxis(min=0, max=1.5, label=r'Q / nm\S-1')
     p[0].title('RMSA structure factor')
     p[0].subtitle(f'R={R:.1f} gamma={gamma0:.1f} eta={eta0:.2f} scl={scl0:.2f}')
     #p.save(js.examples.imagepath+'/rmsa.jpg',size=[600,900])

    .. image:: ../../examples/images/rmsa.jpg
     :width: 50 %
     :align: center
     :alt: rmsa

    References
    ----------
    .. [1] J. B. Hayter and J. Penfold, Mol. Phys. 42, 109 (1981).
    .. [2] J.-P. Hansen and J. B. Hayter, Mol. Phys. 46, 651 (2006).
    .. [3] Jscatter, a program for evaluation and analysis of experimental data
           R.Biehl, PLOS ONE, 14(6), e0218789, 2019,  https://doi.org/10.1371/journal.pone.0218789
    .. [4] L. Belloni, J. Phys. Condens. Matter 12, R549 (2000).

    """

    """
    Original Doc of the Hayter Penfold Fortran routine::
        
    seta is the rescaled volume fraction.                             
    sgek is the rescaled contact potential.                           
    sak is the rescaled screening constant.                           
    a,b,c,f,u,v are the msa coefficients.                             
    g1=g(1+) is the contact value of g(r/sig);                        
    for the Gillan condition, the difference from                     
    zero indicates the computational accuracy.                        

      ROUTINE TO CALCULATE S(Q*SIG) FOR A SCREENED COULOMB
      POTENTIAL BETWEEN FINITE PARTICLES OF DIAMETER 'SIG'
      AT ANY VOLUME FRACTION. THIS ROUTINE IS MUCH MORE POWER-
      FUL THAN "SQHP" AND SHOULD BE USED TO REPLACE THE LATTER
      IN EXISTING PROGRAMS. NOTE THAT THE COMMON AREA IS
      CHANGED; IN PARTICULAR, THE POTENTIAL IS PASSED
      DIRECTLY AS 'GEK' = GAMMA*EXP(-K) IN THE PRESENT ROUTINE.
      JOHN B.HAYTER (I.L.L.) 19-AUG-81
 
      CALLING SEQUENCE:
       CALL SQHPA(QQ,SQ,NPT,IERR)
 
      QQ: ARRAY OF DIMENSION NPT CONTAINING THE VALUES  OF Q*SIG AT WHICH S(Q*SIG) WILL BE CALCULATED.
      SQ: ARRAY OF DIMENSION NPT INTO WHICH VALUES OF  S(Q*SIG) WILL BE RETURNED.
      NPT: NUMBER OF VALUES OF Q*SIG.
 
      IERR > 0: NORMAL EXIT; IERR=NUMBER OF ITERATIONS.
       -1: NEWTON ITERATION NON-CONVERGENT IN "SQCOEF"
       -2: NEWTON ITERATION NON-CONVERGENT IN "SQFUN".
       -3: CANNOT RESCALE TO G(1+) > 0.
 
      ON ENTRY:
      ETA: VOLUME FRACTION
      GEK: THE CONTACT POTENTIAL GAMMA*EXP(-K)
      AK: THE DIMENSIONLESS SCREENING CONSTANT
      AK = KAPPA*SIG WHERE KAPPA IS THE INVERSE SCREENING
      LENGTH AND SIG IS THE PARTICLE DIAMETER.
 
      ON EXIT:
      GAMK IS THE COUPLING: 2*GAMMA*S*EXP(-K/S), S=ETA**(1/3).
      SETA, SGEK AND SAK ARE THE RESCALED INPUT PARAMETERS.
      SCAL IS THE RESCALING FACTOR: (ETA/SETA)**(1/3).
      G1=G(1+), THE CONTACT VALUE OF G(R/SIG).
      A,B,C,F,U,V ARE THE CONSTANTS APPEARING IN THE ANALYTIC
      SOLUTION OF THE MSA (HAYTER-PENFOLD; MOL.PHYS. 42: 109 (1981))
 
      NOTES:
      (A) AFTER THE FIRST CALL TO SQHPA, S(Q*SIG) MAY BE EVALUATED
      AT OTHER Q*SIG VALUES BY REDEFINING THE ARRAY QQ AND CALLING
      "SQHCAL" DIRECTLY FROM THE MAIN PROGRAM.
      (B) THE RESULTING S(Q*SIG) MAY BE TRANSFORMED TO G(R/SIG)
      USING THE ROUTINE "TROGS".
      (C) NO ERROR CHECKING OF INPUT PARAMETERS IS PERFORMED;
      IT IS THE RESPONSIBILITY OF THE CALLING PROGRAM TO VERIFY
      VALIDITY.
      SUBROUTINES REQUIRED BY SQHPA:
      (1) SQCOEF RESCALES THE PROBLEM AND CALCULATES THE
       APPROPRIATE COEFFICIENTS FOR "SQHCAL".
      (2) SQFUN CALCULATES VARIOUS VALUES FOR "SQCOEF".
      (3) SQHCAL CALCULATES H-P S(Q*SIG) GIVEN A,B,C,F.


    """
    R = abs(R)
    error = {-1: 'NEWTON ITERATION NON-CONVERGENT IN _sqcoef',
             -2: 'NEWTON ITERATION NON-CONVERGENT IN _sqfun',
             -3: 'CANNOT RESCALE TO G(1+) > 0.',
             -4: 'no physical root with G(r<1) < 0.1 in _sqfun found'}  # added for new algorithm
    # get volume fraction eta from number density and radius R
    if isinstance(molarity, numbers.Number):
        molarity = abs(molarity)
        numdens = constants.N_A * molarity * 1e-24  # from mol/l to particles/nm**3
        eta = 4 / 3. * np.pi * R ** 3 * numdens
    elif isinstance(eta, numbers.Number):
        numdens = eta / (4 / 3. * np.pi * R ** 3)
        molarity = numdens / (constants.N_A * 1e-24)
    else:
        raise Exception('one of molarity/eta needs to be given.')  # dimensionless screening constant ak
    if eta <= 0.: eta = 1e-10
    # if eta>1:        raise Exception('eta needs to be smaller 1.')
    if scl <= 0:
        ak = 1e20
    else:
        ak = 2 * R / scl
    # to large ak make math error in exp , anyway then we have a hard sphere
    if ak > 200: ak = 200
    # the contact potential in kT
    gek = gamma * math.exp(-ak)
    # coupling
    gamk = 2. * eta ** (1 / 3.) * gek * math.exp(ak - ak / eta ** (1 / 3.))
    # ----------do the rescaling in _sqcoef--------------------
    # _sqcoef does the rescaling to satisfy the Gillian condition with g1==0 according to [2]
    # therein _sqfun calculates the NOT rescaled solution described in [1]
    if useHP:
        ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = _sqcoefOriginalHP(ir=0, eta=eta, gek=gek,
                                                                                                ak=ak, gamk=gamk)
    else:
        ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1 = _sqcoef(ir=0, eta=eta, gek=gek, ak=ak,
                                                                                      gamk=gamk)
    # catch error
    if ir < 0:
        print(ir, error[ir], 'g+ =', g1, 'ak=', ak)
        return ir

    # dimensionless q scale
    q = np.atleast_1d(q)
    qR2 = 2 * R * q
    # calc values by _SQMSA
    sq = _SQMSA(qR2, scal, seta, sak, sgek, a, b, c, f)
    result = dA(np.r_[[q, sq]])
    result.setColumnIndex(iey=None)
    # add important parameters
    result.volumeFraction = eta
    result.rescaledVolumeFraction = seta
    result.molarity = molarity
    result.screeningLength = scl
    result.gamma = gamma
    result.contactpotential = gek
    result.S0 = -1 / a
    result.scalingfactor = scal
    result.gplus1 = [g1, ir]
    result.modelname = inspect.currentframe().f_code.co_name
    result._coefficients = {key: value for (value, key) in
                            zip([ir, eta, gek, ak, a, b, c, f, u, v, gamk, seta, sgek, sak, scal, g1],
                                ['ir', 'eta', 'gek', 'ak', 'a', 'b', 'c', 'f', 'u', 'v', 'gamk', 'seta', 'sgek', 'sak',
                                 'scal', 'g1'])}
    return result


def sq2gr(Sq, R, interpolatefactor=2):
    r"""
    Radial distribution function g(r) from structure factor S(q).

    The result strongly depends on quality of S(Q) (number of data points, Q range, smoothness).
    Read [2]_ for details of this inversion problem and why it may fail.

    Parameters
    ----------
    Sq : dataArray
        Structure factor e.g. in units as [Q]=1/nm
         - .X wavevector
         - .Y structure factor
         - **Advice** : Use more than :math:`2^12` points and :math:`q_{max}R>=100` for accurate results.
    R : float
        Estimate for the radius of the particles.
    interpolatefactor : int
        Number of points between points in interpolation for rfft.
        2 doubles the points

    Returns
    -------
    dataArray
        .n0  approximated from :math:`2\pi^2 n_0=\int_0^{Q_{max}}  [S(Q) -1]Q^2 dQ`

    Notes
    -----
    One finds that

    .. math:: g(r)-1=(2\pi^2 n_0 r)^{-1} \int_0^\infty  [S(Q) -1]Qsin(qr)dQ

    with :math:`2\pi^2 n_0=\int_0^\infty  [S(Q) -1]Q^2 dQ` defining :math:`n_0`.

    As we have only a limited Q range (:math:`0 < Q < \infty` ), limited accuracy and number of Q values
    we require that :math:`mean(g(R/2<r<R3/4))=0`.


    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     p=js.grace()
     p.multi(2,1)
     q=js.loglist(0.01,100,2**13)
     p[0].clear();p[1].clear()
     R=2.5
     eta=0.3;scl=5
     n=eta/(4/3.*np.pi*R**3)   # unit 1/nm**3
     sf=js.sf.RMSA(q=q,R=R,scl=scl, gamma=50, eta=eta)
     gr=js.sf.sq2gr(sf,R,interpolatefactor=1)
     sfcut=js.sf.RMSA(js.loglist(0.01,10,2**10),R=R,scl=scl, gamma=50, eta=eta)
     grcut=js.sf.sq2gr(sfcut,R,interpolatefactor=5)
     p[0].plot(sf.X*2*R,sf.Y,le=r'\xG=50')
     p[1].plot(gr.X/2/R,gr[1],le=r'\xG=50')
     p[1].plot(grcut.X/2/R,grcut[1],le=r'\xG=50 \f{}Q\smax\N=10')
     sfh=js.sf.RMSA(q=q,R=R,scl=scl, gamma=0.01, eta=eta)
     grh=js.sf.sq2gr(sfh,R,interpolatefactor=1)
     p[0].plot(sfh.X*2*R,sfh.Y,le=r'\xG=0.01')
     p[1].plot(grh.X/2/R,grh[1],le=r'\xG=0.01')
     p[0].xaxis(max=20,label='2RQ')
     p[1].xaxis(max=4*R,label='r/(2R)')
     p[0].yaxis(max=2,min=0,label='S(Q)')
     p[1].yaxis(max=2.5,min=0,label='g(r)')
     p[0].legend(x=10,y=1.8)
     p[1].legend(x=4,y=2.2)
     p[0].title('Comparison RMSA')
     p[0].subtitle('R=%.2g, eta=%.2g, scl=%.2g' %(R,eta,scl))
     #p.save(js.examples.imagepath+'/sq2gr.jpg')

    .. image:: ../../examples/images/sq2gr.jpg
     :align: center
     :height: 300px
     :alt: sq2gr

    References
    ----------
    .. [1] Yarnell, J. L., Katz, M. J., Wenzel, R. G., & Koenig, S. H. (1973).
           Structure factor and radial distribution function for liquid argon at 85 K.
           Physical Review A, 7(6), 2130.
    .. [2] On the determination of the pair correlation function from liquid structure factor measurements
            A.K. Soper Chemical Physics 107, 61-74, (1986)

    """
    nn = interpolatefactor * Sq.X.shape[0]
    delta = Sq.X.max() / nn
    Q = np.r_[0:Sq.X.max():1j * nn]
    rrr = 2 * np.pi * scipy.fft.fftfreq(nn, delta)[1:nn // 2]
    # interpolation for more or smoother points
    Yminus1 = np.interp(Q, Sq.X, Sq.Y - 1)
    # Yminus1=scipy.interpolate.interp1d(Sq.X,Sq.Y-1,kind=2)(Q)
    #  doing sine transform to solve the sin integral
    Sqdst = scipy.fft.dst(Yminus1 * Q)
    gr = 1 / (2 * np.pi ** 2 * rrr) * Sqdst[2::2] / (2 * np.pi)
    # grminus=1/(2*np.pi**2*rrr)*Sqdst[3::2]/(2*np.pi)
    n0 = -1 / (2 * np.pi ** 2) * scipy.integrate.simps(Sq.X ** 2 * (Sq.Y - 1), Sq.X)
    factor = abs(gr[abs(rrr - R) < R / 2].mean())
    gr = 1 + gr / factor
    # grminus=1+grminus/factor
    result = dA(np.c_[rrr, gr].T)
    result.n0 = n0
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def PercusYevick(q, R, molarity=None, eta=None):
    """
    The Percus-Yevick structure factor of a hard sphere in 3D.

    Structure factor for the potential U(r)= (inf for 0<r<R) and (0 for R<r).

    Parameters
    ----------
    q : array; N dim
        scattering vector; units 1/(R[unit])
    R : float
        Radius of the object
    eta : float
        volume fraction as eta=4/3*pi*R**3*n  with number density n in units or R
    molarity : float
        number density in mol/l and defines q and R units to 1/nm and nm to be correct
        preferred over eta if both given

    Returns
    -------
    dataArray
        structure factor for given q

    Examples
    --------
    ::

     import jscatter as js
     R = 6
     phi = 0.05
     depth = 15
     q = js.loglist(0.01, 2, 200)
     p = js.grace(1,1)
     for eta in [0.005,0.01,0.03,0.05,0.1,0.2,0.3,0.4]:
         py = js.sf.PercusYevick(q, R, eta=eta)
         p.plot(py, symbol=0, line=[1, 3, -1], legend=f'eta ={eta:.3f}')
     p.yaxis(min=0.0, max=2.2, label='S(Q)', charsize=1.5)
     p.legend(x=1, y=0.9)
     p.xaxis(min=0, max=1.5)
     p.title('3D Percus-Yevick structure factor')
     #p.save(js.examples.imagepath+'/PercusYevick.jpg')

    .. image:: ../../examples/images/PercusYevick.jpg
     :width: 50 %
     :align: center
     :alt: PercusYevick


    Notes
    -----
    Problem is given in [1]_; solution in [2]_ and best description of the solution is in [3]_.

    References
    ----------
    .. [1] J. K. Percus and G. J. Yevick, Phys. Rev. 110, 1 (1958).
    .. [2] M. S. Wertheim, Phys. Rev. Lett. 10, 321 (1963).
    .. [3] D. J. Kinning and E. L. Thomas, Macromolecules 17, 1712 (1984).

    """
    q = np.atleast_1d(q)
    R = abs(R)
    # get volume fraction eta from number density and radius R
    if isinstance(molarity, numbers.Number):
        molarity = abs(molarity)
        numdens = constants.N_A * molarity * 1e-24  # from mol/l to particles/nm**3
        eta = 4 / 3. * np.pi * R ** 3 * numdens
    elif isinstance(eta, numbers.Number):
        eta = abs(eta)
        numdens = eta / (4 / 3. * np.pi * R ** 3)
        molarity = numdens / (constants.N_A * 1e-24)
    else:
        raise Exception('one of molarity/eta needs to be given.')
    if R == 0 or eta == 0:
        Sq = np.ones_like(q)
        a = 1.
    else:
        u = q * R * 2
        u = np.where(u >= 0.01, u, np.ones_like(u) * 0.01)  # problems with number limits for to small u and avoid zero
        a = (1 + 2 * eta) ** 2 / (1 - eta) ** 4
        b = -3 / 2 * eta * (eta + 2) ** 2 / (1 - eta) ** 4
        UU = (a * (np.sin(u) - u * np.cos(u)) +
              b * ((2 / u ** 2 - 1) * u * np.cos(u) + 2 * np.sin(u) - 2 / u) +
              eta * a / 2 * (24 / u ** 3 + 4 * (1 - 6 / u ** 2) * np.sin(u) -
                             (1 - 12 / u ** 2 + 24 / u ** 4) * u * np.cos(u)))
        _Sq = 1 / (1 + 24 * eta / u ** 3 * UU)
        Sq = np.where(u > 0.02, _Sq, np.ones_like(u) / a)  # for low u we use the S(q=0) = 1/a
    result = dA(np.r_[[q, Sq]])
    result.setColumnIndex(iey=None)
    result.modelname = inspect.currentframe().f_code.co_name
    result.eta = eta
    result.molarity = molarity
    result.radius = R
    result.Sq0 = 1 / a
    return result


def PercusYevick2D(q, R=1, eta=0.1, a=None):
    """
    The PercusYevick structure factor of a hard sphere in 2D.

    Structure factor for the potential U(r)= (inf for 0<r<R) and (0 for R<r).

    Parameters
    ----------
    q : array; N dim
        scattering vector; units 1/(R[unit])
    R : float, default 1
        Radius of the object
    eta : float, default 0.1
        packing fraction as eta=pi*R**2*n  with number density n
        maximum hexagonal closed = (np.pi*R**2)/(3/2.*3**0.5*a**2)
        Rmax=a*3**0.5/2. with max packing of 0.9069
    a : float, default None
        hexagonal lattice constant
        if not None the packing fraction in hexagonal lattice
        as eta=(np.pi*R**2)/(3/2.*3**0.5*a**2) is used

    Returns
    -------
    dataArray

    Examples
    --------
    ::

     import jscatter as js
     R = 6
     phi = 0.05
     depth = 15
     q = js.loglist(0.01, 2, 200)
     p = js.grace(1,1)
     for eta in [0.005,0.01,0.03,0.05,0.1,0.2,0.3,0.4]:
         py = js.sf.PercusYevick2D(q, R, eta=eta)
         p.plot(py, symbol=0, line=[1, 3, -1], legend=f'eta ={eta:.3f}')
     p.yaxis(min=0.0, max=2.2, label='S(Q)', charsize=1.5)
     p.legend(x=1, y=0.9)
     p.xaxis(min=0, max=1.5)
     p.title('2D Percus-Yevick structure factor')
     #p.save(js.examples.imagepath+'/PercusYevick2D.jpg')

    .. image:: ../../examples/images/PercusYevick2D.jpg
     :width: 50 %
     :align: center
     :alt: PercusYevick2D


    References
    ----------
    .. [1] Free-energy model for the inhomogeneous hard-sphere fluid in D dimensions:
           Structure factors for the hard-disk (D=2) mixtures in simple explicit form
           Yaakov Rosenfeld Phys. Rev. A 42, 5978

    """
    if a is not None:
        eta = (np.pi * R ** 2) / (3 / 2. * 3 ** 0.5 * a ** 2)
    q = np.atleast_1d(q)
    if R == 0 or eta == 0:
        Sq = np.ones_like(q)
    else:
        qR = lambda q: q * R
        u = np.piecewise(q, [q == 0], [1e-8, qR])  # exchange q=zero with small Q as limit
        Xi = (1 + eta) / (1 - eta) ** 3
        G = (1 - eta) ** -1
        Z = (1 - eta) ** -2
        A = (1 + (2 * eta - 1) * Xi + 2 * eta * G) / eta
        B = ((1 - eta) * Xi - 1 - 3 * eta * G) / eta
        UU = 4 * eta * (
                A * (special.j1(u) / u) ** 2 + B * special.j0(u) * special.j1(u) / u + G * special.j1(2 * u) / u)
        Sq = 1 / (1 + UU)
    result = dA(np.r_[[q, Sq]])
    result.setColumnIndex(iey=None)
    result.packingfraction = eta
    result.R = R
    result.a = (np.pi * R ** 2 / (eta * 3 / 2. * 3 ** 0.5)) ** 0.5
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def PercusYevick1D(q, R=1, eta=0.1):
    """
    The PercusYevick structure factor of a hard sphere in 1D.

    Structure factor for the potential U(r)= (inf for 0<r<R) and (0 for R<r).

    Parameters
    ----------
    q : array; N dim
        scattering vector; units 1/(R[unit])
    R : float
        Radius of the object in nm.
    eta : float
        Packing fraction as eta=2*R*n  with number density n.

    Returns
    -------
    dataArray
        [q,structure factor]

    Examples
    --------
    ::

     import jscatter as js
     R = 6
     phi = 0.05
     depth = 15
     q = js.loglist(0.01, 2, 200)
     p = js.grace(1,1)
     for eta in [0.005,0.01,0.03,0.05,0.1,0.2,0.3,0.4]:
         py = js.sf.PercusYevick1D(q, R, eta=eta)
         p.plot(py, symbol=0, line=[1, 3, -1], legend=f'eta ={eta:.3f}')
     p.yaxis(min=0.0, max=2.2, label='S(Q)', charsize=1.5)
     p.legend(x=1, y=0.9)
     p.xaxis(min=0, max=1.5)
     p.title('1D Percus-Yevick structure factor')
     #p.save(js.examples.imagepath+'/PercusYevick1D.jpg')

    .. image:: ../../examples/images/PercusYevick1D.jpg
     :width: 50 %
     :align: center
     :alt: PercusYevick1D


    References
    ----------
    .. [1] Exact solution of the Percus-Yevick equation for a hard-core fluid in odd dimensions
           Leutheusser E  Physica A 1984 vol: 127 (3) pp: 667-676
    .. [2] On the equivalence of the Ornstein–Zernike relation and Baxter’s relations for a one-dimensional simple fluid
           Chen M Journal of Mathematical Physics 1975 vol: 16 (5) pp: 1150

    """
    q = np.atleast_1d(q)
    D = 2. * R
    nn = eta / D
    if R == 0 or eta == 0:
        Sq = np.ones_like(q)
    else:
        # exchange q=zero with small Q as limit
        Q = np.piecewise(q, [q == 0], [1e-8, lambda q: q])
        xi = (1 - D * nn)
        cQ = -2 * (1. / Q / xi * np.sin(Q * D) + nn / Q ** 2 / xi ** 2 * (1 - np.cos(Q * D)))
        Sq = (1 - cQ * nn) ** -1  # =1/A eq 6 and 8b of [1]_
    result = dA(np.r_[[q, Sq]])
    result.setColumnIndex(iey=None)
    result.packingfraction = eta
    result.R = R
    result.nkTkappa = xi ** 2
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def stickyHardSphere(q, R, width, depth, molarity=None, phi=None):
    r"""
    Structure factor of a square well potential with depth and width (sticky hard spheres).

    Sticky hard sphere model is derived using a perturbative solution of the factorized
    form of the Ornstein-Zernike equation and the Percus-Yevick closure relation.
    The perturbation parameter is width/(width+2R)

    Parameters
    ----------
    q : array; N dim
        Scattering vector; units 1/(R[unit])
    R : float
        Radius of the hard sphere
    phi : float
        Volume fraction of the hard core particles
    molarity : float
        Number density in mol/l and defines q and R units to 1/nm and nm to be correct
        Preferred over phi if both given.
    depth : float
        Potential well depth in kT
        depth >0 (U<0); positive potential allowed (repulsive) see [1]_.
    width : float
        Width of the square well

    Notes
    -----
    The potential U(r) is defined as

    .. math::       U(r) &= \infty        & r<2R  \\

                         &= -depth[kT]    & 2R<r<2R+width \\

                         &= 0               & r>2R+width

    Other definitions include
     - eps=width/(2*R+width)
     - stickiness=exp(-depth)/12./eps

    Examples
    --------
    ::

     import jscatter as js
     R = 6
     phi = 0.05
     depth = 15
     q = js.loglist(0.01, 2, 200)
     p = js.grace(1,1)
     for eta in [0.005,0.01,0.03,0.05,0.1,0.2]:
         shs = js.sf.stickyHardSphere(q, R, 1, 3, phi=eta)
         p.plot(shs, symbol=0, line=[1, 3, -1], legend=f'eta ={eta:.3f}')
     p.yaxis(min=0.0, max=3.2, label='S(Q)', charsize=1.5)
     p.legend(x=1, y=3)
     p.xaxis(min=0, max=1.5)
     p.title('sticky hard sphere structure factor')
     #p.save(js.examples.imagepath+'/stickyHardSphere.jpg')

    .. image:: ../../examples/images/stickyHardSphere.jpg
     :width: 50 %
     :align: center
     :alt: stickyHardSphere


    References
    ----------
    .. [1] S.V. G. Menon, C. Manohar, and K. S. Rao, J. Chem. Phys. 95, 9186 (1991)
    .. [2] M. Sztucki, T. Narayanan, G. Belina, A. Moussaïd, F. Pignon, and H. Hoekstra, Phys. Rev. E 74, 051504 (2006)
    .. [3] W.-R. Chen, S.-H. Chen, and F. Mallamace, Phys. Rev. E 66, 021403 (2002)
    .. [4] G. Foffi, E. Zaccarelli, F. Sciortino, P. Tartaglia, and K. A. Dawson, J. Stat. Phys. 100, 363 (2000)

    """
    # get volume fraction eta from number density and radius R
    if isinstance(molarity, numbers.Number):
        numdens = constants.N_A * molarity * 1e-24  # from mol/l to particles/nm**3
        phi = 4 / 3. * np.pi * R ** 3 * numdens
    elif isinstance(phi, numbers.Number):
        numdens = phi / (4 / 3. * np.pi * R ** 3)
        molarity = numdens / (constants.N_A * 1e-24)
    else:
        raise Exception('one of molarity/eta needs to be given.')

    # to prevent math errors
    if depth < -200: depth = -200

    q = np.atleast_1d(q)
    Q = np.piecewise(q, [q == 0], [1e-8, lambda q: q])  # avoid zero

    eps = width / (2 * R + width)  # perturbation parameter
    if eps == 0: eps = 1e-10
    tau = math.exp(-depth) / 12. / eps  # stickiness
    eta = phi * (1 - eps) ** 3
    lam = (1 + 0.5 * eta) / (1 - eta) ** 2 / (eta ** 2 / (1 - eta) - eta / 12. + tau)
    mu = lam * eta * (1 - eta)
    al = (1 + 2 * eta - mu) / (1 - eta) ** 2
    be = (-3 * eta + mu) / 2. / (1 - eta) ** 2
    k = Q * (2 * R + width)

    sink = np.sin(k)
    cosk = np.cos(k)
    Ak = 1 + 12 * eta * (al * ((sink - k * cosk) / k ** 3) + be * (1 - cosk) / k ** 2 - lam / 12. * sink / k)
    Bk = 12 * eta * (al * (0.5 / k - sink / k ** 2 + (1 - cosk) / k ** 3) + be * (1 / k - sink / k ** 2) -
                     lam / 12. * ((1 - cosk) / k))
    Sk = 1. / (Ak * Ak + Bk * Bk)

    result = dA(np.r_[[q, Sk]])
    result.welldepth = depth
    result.weelwidth = width
    result.stickiness = tau
    result.volumefraction = phi
    result.eta = eta
    result.molarity = molarity
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def adhesiveHardSphere(q, R, tau, delta, molarity=None, eta=None):
    r"""
    Structure factor of a adhesive hard sphere potential (a square well potential)


    Parameters
    ----------
    q : array; N dim
        scattering vector; units 1/(R[unit])
    R : float
        radius of the hard core
    eta : float
        volume fraction of the hard core particles
    molarity : float
        number density in mol/l and defines q and R units to 1/nm and nm to be correct
        preferred over eta if both given
    tau : float
        stickiness
    delta : float
        width of the square well

    Notes
    -----
    The potential U(r) is defined as

    .. math::       U(r) &= \infty        & r<2R  \\

                         &=-depth=ln(12*tau*delta/(2R+delta))    & 2R<r<2R+width \\

                         &= 0               & r>2R+width

    Examples
    --------
    ::

     import jscatter as js
     R = 6
     phi = 0.05
     depth = 15
     q = js.loglist(0.01, 2, 200)
     p = js.grace(1,1)
     for eta in [0.005,0.01,0.03,0.05,0.1,0.2]:
         shs = js.sf.adhesiveHardSphere(q, R, 1, 3, eta=eta)
         p.plot(shs, symbol=0, line=[1, 3, -1], legend=f'eta ={eta:.3f}')
     p.yaxis(min=0.0, max=3.2, label='S(Q)', charsize=1.5)
     p.legend(x=1, y=3)
     p.xaxis(min=0, max=1.5)
     p.title('adhesive hard sphere structure factor')
     #p.save(js.examples.imagepath+'/adhesiveHardSphere.jpg')

    .. image:: ../../examples/images/adhesiveHardSphere.jpg
     :width: 50 %
     :align: center
     :alt: adhesiveHardSphere


    References
    ----------
    .. [1] C. Regnaut and J. C. Ravey, J. Chem. Phys. 91, 1211 (1989).
    .. [2] C. Regnaut and J. C. Ravey, J. Chem. Phys. 92 (5) (1990), 3250 Erratum

    """
    # get volume fraction eta from number density and radius R
    if isinstance(molarity, numbers.Number):
        numdens = constants.N_A * molarity * 1e-24  # from mol/l to particles/nm**3
        eta = 4 / 3. * np.pi * R ** 3 * numdens
    elif isinstance(eta, numbers.Number):
        numdens = eta / (4 / 3. * np.pi * R ** 3)
        molarity = numdens / (constants.N_A * 1e-24)
    else:
        raise Exception('one of molarity/eta needs to be given.')
    q = np.atleast_1d(q)

    sigma = 2. * R + delta
    k = np.piecewise(q, [q == 0], [1e-8, lambda q: q * sigma])
    phi = eta * (sigma / (2 * R)) ** 3

    lam = 6. * (tau / phi + 1.0 / (1. - phi))
    try:
        lam1 = lam + math.sqrt(lam ** 2 - 12. / phi * (1. + 0.5 * phi) / (1 - phi) ** 2)
        lam2 = lam - math.sqrt(lam ** 2 - 12. / phi * (1. + 0.5 * phi) / (1 - phi) ** 2)
        lambd = lam1 if abs(lam1) < abs(lam2) else lam2
    except ValueError:  # complex root
        return -1

    mu = lambd * phi * (1. - phi)
    A = 0.5 * (1. + 2. * phi - mu) / (1. - phi) ** 2
    B = 0.5 * sigma * (mu - 3. * phi) / (1. - phi) ** 2
    C = -A * sigma ** 2 - B * sigma + lambd * sigma ** 2 / 12.

    sink = np.sin(k)
    cosk = np.cos(k)
    I0 = sink / k
    I1 = (cosk + k * sink - 1.0) / k ** 2
    I2 = (k ** 2 * sink - 2.0 * sink + 2.0 * k * cosk) / k ** 3
    J0 = (1 - cosk) / k
    J1 = (sink - k * cosk) / k ** 2
    J2 = (2. * sink * k + 2. * cosk - k ** 2 * cosk - 2.) / k ** 3

    alpha = 1.0 - 12.0 * phi * (C / sigma ** 2 * I0 + B / sigma * I1 + A * I2)
    beta = 12.0 * phi * (C / sigma ** 2 * J0 + B / sigma * J1 + A * J2)

    SQ = 1. / (alpha * alpha + beta * beta)

    result = dA(np.r_[[q, SQ]])
    try:
        result.welldepth = math.log(12 * tau * delta / sigma)
    except ZeroDivisionError:
        result.welldepth = -np.inf
    result.wellwidth = delta
    result.stickiness = tau
    result.welldepth = math.log(12 * tau * delta / sigma) if 12 * tau * delta / sigma > 0 else np.inf
    result.HSvolumefraction = eta
    result.phi = phi
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def criticalSystem(q, cl, itc):
    r"""
    Structure factor of a critical system according to the Ornstein-Zernike form.

    Parameters
    ----------
    q : array; N dim
        Scattering vector; units 1/(cl[unit])
    cl : float
        Correlation length in units nm.
    itc : float
        Isothermal compressibility of the system.

    Notes
    -----

    .. math:: S(q) = \frac{itc}{1+q^2 cl^2}

    - The peaking of the structure factor near Q=0 region is due to attractive interaction.
    - Away from it the structure factor should be close to the hard sphere structure factor.
    - Near the critical point we should find
      :math:`S(q)=S_{PY}(q)+S_{OZ}(q)`
       - :math:`S_{PY}` Percus Yevick structure factor
       - :math:`S_{OZ}` this function

    References
    ----------
    .. [1] Analysis of Critical Scattering Data from AOT/D2O/n-Decane Microemulsions
           S. H. Chen, T. L. Lin, M. Kotlarchyk
           Surfactants in Solution pp 1315-1330

    """
    Q = np.atleast_1d(q)
    result = dA(np.r_[[Q, itc / (1 + Q ** 2 * cl ** 2)]])
    result.corrlength = cl
    result.isothermalcompress = itc
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def _LhklVoigt(q, center, lg, domainsize, asym):
    # Voigt bragg peak shape
    return formel.voigt(q, center=center, lg=lg, fwhm=2 * np.pi / domainsize, asym=asym).Y


def latticeStructureFactor(q, lattice=None, domainsize=1000, asym=0, lg=1, rmsd=0.02, beta=None,
                           hklmax=7, c=1., wavelength=None, corrections=[]):
    r"""
    Radial structure factor S(q) in powder average of a crystal lattice with particle asymmetry,
    DebyeWaller factor, diffusive scattering and broadening due to domain size.

    - To get the full scattering the formfactor needs to be included (See Notes and Examples).
    - 1-3 dimensional lattice structures with basis containing multiple atoms (see lattice).
    - Self absorption and self extinction are not included. Polarisation and Lorentz correction are optional.
    - **How to fit see last example** `latticeStructureFactor as a fit model`_ .

    Parameters
    ----------
    q : array float
        Norm of wavevectors in inverse units of lattice constant, units 1/nm
    domainsize : float
        Domainsize of the crystal, units as lattice constant of lattice.
        According to Debye-Scherrer equation :math:`fwhm=2\pi/domainsize` the peak width is determined [2]_.
    lattice : lattice object
        The crystal structure as defined in a lattice object. The size of the lattice is ignored. One of
        rhombicLattice, bravaisLattice, scLattice, bccLattice, fccLattice, diamondLattice, hexLattice, hcpLattice.
        See respective definitions.
    lg : float, default = 1
        Lorenzian/gaussian fraction describes the contributions of gaussian and lorenzian
        shape in peak shape (Voigt function).
         - lorenzian/gaussian >> 1  lorenzian,
         - lorenzian/gaussian ~  1  central part gaussian, outside lorenzian wings
         - lorenzian/gaussian << 1  gaussian
    asym : float, default=0
        Asymmetry factor in sigmoidal as :math:`2fwhm/(1+e^{asym*(x-center)})`
        For asym=0 the Voigt is symmetric with fwhm. See formel.voigt .
    rmsd : float, default=0.02
        Root mean square displacement :math:`rmsd=<u^2>^{0.5}` determining the Debye Waller factor.
        Units as domainsize and lattice units.
        Here Debye Waller factor is used as :math:`DW(q)=e^{-q^2 rmsd^2 }`
    beta : float, None, dataArray
        Asymmetry factor of the formfactor or reduction due to polydispersity.
         - None beta=1, No beta assumed (spherical symmetric formfactor, no polydispersity)
         - dataArray explicitly given as dataArray with beta in .Y column.
           Missing values are interpolated.
         - An approximation for polydisperse beta can be found in [1]_ equ.17.
           This can be realized by  beta=js.dA(np.vstack(q,np.exp(-(q*sr*R)**2)))
           with sr as relative standard deviation of gaussian distribution of the size R.
         - See .formfactor for different formfactors which explicit calculation of beta.
    hklmax : int
        Maximum order of the Bragg peaks to include.
    c : float, default=1
        Porod constant. See 3.8 in [1]_.
    wavelength : float, default =  None
        Wavelength of the measurement in units nm. If None .Braggtheta is not calculated.
        For Xray Cu K_a it is 0.15406 nm.
    corrections : list, default=[]
        List of corrections to apply, which depend on the measurement type/geometry [5]_.
        :math:`\theta` is here the scattering angle (not :math:`2\theta` as in diffraction is used)
         - *'TP'* Thompson polarisation correction :math:`(1+cos^2(\theta)/2)` for electromagnetic
           scattering as Xrays [4]_. For small angle scattering this is negligible but valid.
           For polarised beams the polarisation has to be included.
         - *'lh'* likelihood of a crystallite being in diffraction position :math:`cos(\theta/2)`.
         - *'LC'* Lorentz correction :math:`\sin(\theta)^{-1}` due to integration
            over the width of reciprocal Bragg peaks due to lattice imperfections and the width of the incoming
            beam. Use for Debye-Scherrer (powder of crystallites) diffraction.
         - *'area'* the intensity for a given diffraction peak is recorded on a narrow strip of
            photographic film instead of over the entire diffraction cone :math:`\sin(\theta)^{-1}`.
         - *'all'* common Lorentz and polarisation correction powder measurements of crystalline material.
            Use all from above. NOT for flat transmission geometry (typical SAS) or non crystallite .
           Corresponds to :math:`(1+cos^2(\theta)/2)/sin^2(\theta/2)/sin(\theta/2)`.
        The correction for the pixel area presented to scattering solid angle is included in sasImage in
        2D also correcting for offset detector positions of a flat detector,
        which cannot use the scattering angle :math:`\theta` as the geometry changes.

    Returns
    -------
    dataArray
        Columns [q, Sq, DW, beta, Z0q, correction, theta]
         - q wavevector
         - Sq = S(q) = (1+beta(q)*(Z0(q)-1)*DW(q))*correction         structure factor
         - DW(q)   Debye-Waller factor with (1-DW)=diffusive scattering.
         - beta(q)   asymmetry factor of the formfactor.
         - Z0q       lattice factor Z0(q)
         optional
         - correction       [optional] factor polarisation from Thompson scattering
         - theta scattering angle
        Attributes
         - .q_hkl    peak positions
         - .fhkl     symmetry factor
         - .mhkl     multiplicity
         - .Braggtheta   Bragg angles

    Notes
    -----
    Analytical expressions for the scattering functions of **atomic crystals and ordered mesoscopic materials** .
    Ordered  structures  in 3D (fcc,  bcc,  hcp,  sc), 2D (hex, sq) and lamellar structures are considered.
    The expressions take into account particle size distributions and lattice point deviations, domain size,
    core/shell structures, as well as peak shapes varying analytically between Lorentzian and Gaussian functions.
    The expressions allow one to quantitatively describe high-resolution synchrotron small-angle X-ray (SAXS) and
    neutron scattering (SANS) curves from lipid and block copolymer lyotropic phases, core/shell nanoparticle
    superstructures, ordered nanocomposites, ordered mesoporous  materials and atomic crystal structures
    (see AgBe example).

    - The scattering intensity of a crystal domain in powder average is

      .. math:: I(q)={\Delta\rho}^2 n P(q) S(q)

      with
       - :math:`\Delta\rho` scattering length difference between matrix and particles
       - :math:`n` number density (of elementary cells)
       - :math:`P(q)` form factor
       - :math:`S(q)` structure factor :math:`S(q)`
      For inhomogeneous particles or atoms with different scattering length we can incorporate :math:`\Delta\rho(r)`
      in the formfactor :math:`P(q)` if this includes the integrated scattering length differences.
    - The structure factor is [1]_ :

      .. math:: S(q)=1+ \beta(q)(Z_0(q)-1)*DW(Q)

      with
       - :math:`\beta(q)=<F(q)>^2/<F(q)^2>` as asymmetry factor [3]_ dependent on the
         scattering amplitude :math:`F(q)` and particle polydispersity
       -  :math:`DW(q)` Debye Waller factor

    - The lattice factor is [1]_ :

      .. math :: Z_0(q) = \frac{(2\pi)^{d-1}c}{nv_dq^{d-1}} \sum\limits_{hkl}m_{hkl}f_{hkl}^2L_{hkl}(q)

      with
       - :math:`n`           number of particles per unit cell
       - :math:`f_{hkl}`     unit cell structure factor that takes into account symmetry-related extinction rules
       - :math:`v_d`         volume of the d-dimensional unit cell
       - :math:`hkl`         reflections
       - :math:`m_{hkl}`     peak multiplicity
       - :math:`c`           Porod constant :math:`\simeq 1`

    - Unit cell structure factors :math:`f_{hkl}` are normalised that the lattice factor is normalised for
      infinite q to 1. With i as unit cell atoms at fractional position in the unit cell :math:`[x_i,y_i,z_i]`
      and scattering amplitude :math:`b_i` we get :

      .. math:: f_{hkl}^2 = \big(\sum_i b_i e^{-2\pi (hx_i+ky_i+lz_i)}\big)^2 / \sum_i b_i^2

    - We use a Voigt function for the peak shape :math:`L_{hkl}(q)` (see formel.voigt).
    - DW is a Debye Waller like factor as :math:`DW(q)=e^{-q^2<u^2>}` leading to a reduction
      of scattered intensity and diffusive scattering.
      It has contributions from thermal lattice disorder ( DW factor with 1/3 factor in 3D),
      surface roughness and size polydispersity.
    - For the limiting behaviour q->0 see the discussion in [1]_ in 3.9. :
       "... The zero-order peak is not explicitly considered because of the q^(1-dim) singularity and
       because its intensity depends also on the scattering length difference between the lattice inside and outside...
       Due to the singularity and since structural features on length scales d > a,
       such as packing defects, grain boundaries or fluctuations decaying on larger length scales
       are only indirectly considered via the domain size D, eq 30 is not expected to give good agreement with
       experimentally determined scattering curves in the range of scattering vectors q < 2π/a.
       However, for q > 2π/a, this approach describes remarkably well experimentally measured
       high-resolution scattering curves...."

      A good description of the real scattering for low Q is shown in
      example :ref:`A nano cube build of different lattices`.

    Examples
    --------
    Structure factor for *hexagonal lattice* dependent on rmsd
    ::

     import jscatter as js
     import numpy as np
     q = np.r_[0.02:1:800j]
     a = 50.
     R=15
     sr=0.1
     p = js.grace()
     beta=js.dA(np.vstack([q,np.exp(-(q*sr*R)**2)]))
     p.title('structure factor for hexagonal 2D lattice with a={0} nm'.format(a))
     p.subtitle('with diffusive scattering and asymmetry factor beta')
     for i,rmsd in enumerate([1., 3., 10., 30.],1):
         grid=js.sf.scLattice(50,5)
         hex = js.sf.latticeStructureFactor(q, rmsd=rmsd, domainsize=500., beta=beta,lattice=grid)
         p.plot(hex, li=[1, 2, i], sy=0, le='rmsd=$rmsd')
         p.plot(hex.X,1-hex._DW, li=[3, 2, i], sy=0)
     p.plot(hex.X, hex._beta, li=[2, 2, i], sy=0, le='beta')
     p.text(r'broken lines \nshow diffusive scattering',x=0.4,y=6)
     p.yaxis(label='S(q)')
     p.xaxis(label='q / nm')
     p.legend(x=0.6,y=4)

    **Comparison of sc, bcc, fcc** for same cubic unit cell size to demonstrate selection rules.
    ::

     import jscatter as js
     import numpy as np
     q=np.r_[js.loglist(0.1,3,200),3:40:800j]
     unitcelllength=1.5
     N=2
     R=0.5
     sr=0.1
     beta=js.dA(np.vstack([q,np.exp(-(q*sr*R)**2)]))
     rmsd=0.02
     #
     scgrid= js.lattice.scLattice(unitcelllength,N)
     sc=js.sf.latticeStructureFactor(q, rmsd=rmsd, domainsize=50., beta=beta,lattice=scgrid)
     bccgrid= js.lattice.bccLattice(unitcelllength,N)
     bcc=js.sf.latticeStructureFactor(q, rmsd=rmsd, domainsize=50., beta=beta,lattice=bccgrid)
     fccgrid= js.lattice.fccLattice(unitcelllength,N)
     fcc=js.sf.latticeStructureFactor(q, rmsd=rmsd, domainsize=50., beta=beta,lattice=fccgrid)
     #
     p=js.grace()
     p.plot(sc,legend='sc')
     p.plot(bcc,legend='bcc')
     p.plot(fcc,legend='fcc')
     p.yaxis(label='S(q)',scale='l',max=50,min=0.05)
     p.xaxis(label='q / nm',scale='l',max=50,min=0.5)
     p.legend(x=1,y=30,charsize=1.5)
     # p.save(js.examples.imagepath+'/latticeStructureFactor2.jpg')

    .. image:: ../../examples/images/latticeStructureFactor2.jpg
     :align: center
     :height: 300px
     :alt: multiParDistributedAverage

    A realistic example of a **calibration measurement with AgBe**.
    We load the cif file of the crystal structure to build the lattice and find good agreement.
    According to materialsproject.org calculated XRD tends to underestimate lattice parameters.
    For AgBe the first peak is found at 1.07
    ::

     import jscatter as js
     #
     # Look at raw calibration measurement
     calibration = js.sas.sasImage(js.examples.datapath+'/calibration.tiff')
     bc=calibration.center
     calibration.mask4Polygon([bc[0]+8,bc[1]],[bc[0]-8,bc[1]],[bc[0]-8+60,0],[bc[0]+8+60,0])
     # mask center
     calibration.maskCircle(calibration.center, 18)
     # mask outside shadow
     calibration.maskCircle([500,320], 280,invert=True)
     # calibration.show(axis='pixel',scale='log')
     cal=calibration.radialAverage()
     # lattice from crystallographic data in cif file.
     agbe=js.sf.latticeFromCIF(js.examples.datapath + '/1507774.cif',size=[0,0,0])
     sfagbe=js.sf.latticeStructureFactor(cal.X, lattice=agbe,
                                        domainsize=50, rmsd=0.001, lg=1, hklmax=17,wavelength=0.15406)

     p=js.grace()
     p.plot(cal)
     # add scaling and background (because of unscaled raw data)
     p.plot(sfagbe.X,190*sfagbe.Y+1.9,sy=0,li=[1,3,4])
     p.yaxis(scale='log',label='I(q) / counts/pixel')
     p.xaxis(scale='log',label='q / nm|S-1',min=0.7,max=20)
     p.title('AgBe reference measurements')
     # p.save(js.examples.imagepath+'/latticeStructureFactor.jpg')

    .. image:: ../../examples/images/latticeStructureFactor.jpg
     :align: center
     :height: 300px
     :alt: multiParDistributedAverage

    .. _latticeStructureFactor as a fit model:

    **latticeStructureFactor as a fit model**
    We include the possibility of polydispersity.

    We use a hexagonal lattice with small hex_a lattice constant and large hex_c to mimic a lamellar structure with
    lattice constant 5.833 nm as found for AgBe with main scattering coming from Ag atoms in a plane (z=0).
    The fit results are not as good as the above AgBe example. The fit can be improved limiting it to Q<7.
    This highlights the importance of the atom distribution in the unit cell in the example above.
    ::

     import jscatter as js

     # smearing even for SAXS here with a single width (for one of our SAXS machines).
     fbeam_12=js.sas.prepareBeamProfile(0.035)

     def hexSF(q, hex_c,hex_a, domainsize, rmsd,):
        # hexagonal structure factor
         # first make a lattice (size is later ignored)
         hex = js.sf.hexLattice(ab=hex_a,c=hex_c,size=5)
         # then calculate the structure factor and return it
         sf = js.sf.latticeStructureFactor(q=q, lattice=hex, domainsize=domainsize,
                                           hklmax=17, rmsd=rmsd, wavelength=0.15406)
         return sf

     # This includes a beamprofile for smearing (may be ommited)
     @js.sas.smear(beamProfile=fbeam_12)
     def hexmodel(q, hex_c,hex_a,dc, domainsize, rmsd, bgr, I0):
         if dc >0:
             # include a polydispersity in lattice constant, or wvelength or whatever is reasonable
             # also multiple parameters are possible using mPDA
             result  = js.formel.pDA(hexSF, dc, 'hex_c',q=q,hex_a=hex_a,hex_c=hex_c,domainsize=domainsize,rmsd=rmsd)
         else:
             # no polydispersity, do it direct
             result = hexSF(q=q,hex_a=hex_a,hex_c=hex_c,domainsize=domainsize,rmsd=rmsd)
         result.Y=I0*result.Y+bgr
         return result

     # Use data from agbe from above example
     cal.makeErrPlot(xscale='log',yscale='log')
     cal.setlimit(bgr=[0])
     cal.fit(model=hexmodel,
         freepar={'hex_c':5.8, 'domainsize':50,'rmsd':0.1,'bgr': 2,'I0':3},
         fixpar={'hex_a':0.5,'dc':0,}, mapNames={'q': 'X'},
         method='Nelder-Mead',  # Nelder-Mead is better for these cases
         condition=lambda a:(a.X>0)&(a.X<10))



    References
    ----------
    .. [1] Scattering curves of ordered mesoscopic materials.
           Förster, S. et al. J. Phys. Chem. B 109, 1347–1360 (2005).
    .. [2] Patterson, A.
           The Scherrer Formula for X-Ray Particle Size Determination
           Phys. Rev. 56 (10): 978–982 (1939)
           doi:10.1103/PhysRev.56.978.
    .. [3] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).1
    .. [4] https://en.wikipedia.org/wiki/Thomson_scattering
    .. [5] Modern Physical Metallurgy chapter 5 Characterization and Analysis
           R.E.SmallmanA.H.W.Ngan
           https://doi.org/10.1016/B978-0-08-098204-5.00005-5

    """
    if corrections == 'all' or 'all' in corrections:
        corrections = ['TP', 'lh', 'LC', 'area']

    qq = q.copy()
    qq[q == 0] = min(q[q > 0]) * 1e-4  # avoid zero

    n = len(lattice.unitCellAtoms)
    vd = lattice.unitCellVolume
    dim = len(lattice.latticeVectors)
    qhkl, f2hkl, mhkl, hkl = lattice.getRadialReciprocalLattice(hklmax)

    # lattice factor
    if useFortran:
        # factor 3 faster for single cpu, additional factor 3 for multiprocessing (on 6 core)
        Z0q = fscatter.utils.sumlhklvoigt(qq, qhkl, f2hkl, mhkl, lg, domainsize, asym, dim, c, n, vd, 0)
    else:
        Z0q = np.c_[[m * f2 * _LhklVoigt(qq, qr, lg, domainsize, asym)
                     for qr, f2, m in zip(qhkl, f2hkl, mhkl)]].sum(axis=0)
        Z0q *= (2 * np.pi) ** (dim - 1) * c / n / vd / qq ** (dim - 1)

    # normalisation
    Z0q = Z0q / np.sum(np.r_[lattice.unitCellAtoms_b]**2)

    if beta is None:
        beta = np.ones_like(q)
    elif hasattr(beta, '_isdataArray'):
        beta = beta.interp(q)

    # Debye Waller factor
    DW = np.exp(-q ** 2 * rmsd ** 2)

    # structure factor
    Sq = 1 + beta * (Z0q - 1) * DW

    if wavelength is None:
        # prepare result
        result = dA(np.vstack([q, Sq, DW, beta, Z0q]))
        result.columnname = 'q; Sq; DW; beta; Z0q'
    else:
        theta = 2 * np.arcsin(qq * wavelength / 4. / np.pi)
        correction = np.ones_like(Sq)
        if 'TP' in corrections:
            correction = correction * (1 + np.cos(theta) ** 2) / 2
        if 'LC' in corrections:
            correction = correction / np.sin(theta)
        if 'area' in corrections:
            correction = correction / np.sin(theta)
        if 'lh' in corrections:
            correction = correction * np.cos(theta / 2)
        # prepare result
        result = dA(np.vstack([q, Sq * correction, DW, beta, Z0q, correction, theta]))
        result.columnname = 'q; Sq; DW; beta; Z0q; TPf; theta'

    result.setColumnIndex(iey=None)
    result.q_hkl = qhkl
    result.fhkl = f2hkl
    result.sumfi2 = np.sum(np.r_[lattice.unitCellAtoms_b] ** 2)
    result.mhkl = mhkl
    result.hkl = hkl
    if wavelength is not None:
        result.Braggtheta = lattice.getScatteringAngle(size=hklmax, wavelength=wavelength)
    result.latticeconstants = la.norm(lattice.latticeVectors, axis=1)
    result.peakFWHM = 2 * np.pi / domainsize
    result.peaksigma = (result.peakFWHM / (2 * np.sqrt(2 * np.log(2))))
    result.peakAsymmetry = asym
    result.domainsize = domainsize
    result.rmsd = rmsd
    result.lorenzianOverGaussian = lg
    result.modelname = inspect.currentframe().f_code.co_name
    return result


def radial3DLSF(qxyz, lattice=None, domainsize=1000, asym=0, lg=1, rmsd=0.02, beta=None,
                hklmax=7, c=1., wavelength=None, corrections=[]):
    r"""
    3D structure factor S(q) in powder average of a crystal lattice
    with particle asymmetry, DebyeWaller factor, diffusive scattering and broadening due to domain size.

    The qxyz can be an arbitrary composition of points in reciprocal space.
    Uses latticeStructureFactor. The peak shape is a Voigt function.

    Parameters
    ----------
    qxyz : 3xN array
        Wavevector plane in inverse units of lattice constant, units 1/A or 1/nm.
    domainsize : float
        Domainsize of the crystal, units as lattice constant of lattice.
        According to Debye-Scherrer equation :math:`fwhm=2\pi/domainsize` the peak width is determined [2]_.
    lattice : lattice object
        The crystal structure as defined in a lattice object. The size of the lattice is ignored. One of
        rhombicLattice, bravaisLattice, scLattice, bccLattice, fccLattice, diamondLattice, hexLattice, hcpLattice.
        See respective definitions.
    lg : float, default = 1
        Lorenzian/gaussian fraction describes the contributions of gaussian and lorenzian shape in peak shape.
         - lorenzian/gaussian >> 1  lorenzian,
         - lorenzian/gaussian ~  1  central part gaussian, outside lorenzian wings
         - lorenzian/gaussian << 1  gaussian
    asym : float, default=0
        Asymmetry factor in sigmoidal as :math:`2fwhm/(1+e^{asym*(x-center)})`
        For asym=0 the Voigt is symmetric with fwhm. See formel.voigt .
    rmsd : float, default=0.02
        Root mean square displacement :math:`rmsd=<u^2>^{0.5}` determining the Debye Waller factor.
        Units as domainsize and lattice units.
        Here Debye Waller factor is used as :math:`DW(q)=e^{-q^2 rmsd^2 }`
    beta : float, None, dataArray
        Asymmetry factor of the formfactor or reduction due to polydispersity.
         - None beta=1, No beta assumed (spherical symmetric formfactor, no polydispersity)
         - dataArray explicitly given as dataArray with beta in .Y column.
           Missing values are interpolated.
         - An approximation for polydisperse beta can be found in [1]_ equ.17.
           This can be realized by  beta=js.dA(np.vstack(q,np.exp(-(q*sr*R)**2)))
           with sr as relative standard deviation of gaussian distribution of the size R.
         - See .formfactor for different formfactors which explicit calculation of beta.
    hklmax : int
        Maximum order of the Bragg peaks to include.
    c : float, default=1
        Porod constant. See 3.8 in [1]_.
    wavelength : float, default =  None
        Wavelength of the measurement in units nm. If None .Braggtheta is not calculated.
        For Xray Cu K_a it is 0.15406 nm.
    corrections : list, default=[]
        List of corrections to apply, which depend on the measurement type/geometry.
        See :py:func:`~.sf.latticeStructureFactor`

    Returns
    -------
    dataArray
        Columns [qx,qz,qw,Sq]
         - Sq = S(q) = 1+beta(q)*(Z0(q)-1)*DW(q) structure factor
        Attributes
         - .q_hkl    peak positions
         - .fhkl     symmetry factor
         - .mhkl     multiplicity

    Notes
    -----
        See latticeStructureFactor.

    Examples
    --------
    ::

     import jscatter as js
     import numpy as np
     import matplotlib.pyplot as pyplot
     from matplotlib import cm
     from matplotlib import colors
     norm=colors.LogNorm(clip=True)

     # create lattice
     sclattice = js.lattice.scLattice(2.1, 1)
     ds = 50

     # add flat detector xy plane
     xzw = np.mgrid[-8:8:500j, -8:8:500j]

     qxzw = np.stack([np.zeros_like(xzw[0]), xzw[0], xzw[1]], axis=0)
     ff1 = js.sf.radial3DLSF(qxzw.reshape(3, -1).T, sclattice, domainsize=ds, rmsd=0.03, hklmax=7)
     norm.autoscale(ff1.Y)
     fig = pyplot.figure()
     ax = fig.add_subplot(1, 1, 1)
     im = ax.imshow(ff1.Y.reshape(500,-1),norm=norm)
     fig.colorbar(im, shrink=0.8)
     js.mpl.show()

    Note that for to low number of points in the xzw plane moire patterns appear.
    ::


     import jscatter as js
     import numpy as np

     import matplotlib.pyplot as pyplot
     from matplotlib import cm

     # Set the aspect ratio to 1 so our sphere looks spherical
     fig = pyplot.figure(figsize=pyplot.figaspect(1.))
     ax = fig.add_subplot(111, projection='3d')

     # create lattice
     sclattice = js.lattice.scLattice(2.1, 1)
     ds = 50

     # add flat detector xy plane
     xzw = np.mgrid[-8:8:250j, -8:8:250j]

     qxzw = np.stack([np.zeros_like(xzw[0]), xzw[0], xzw[1]], axis=0)
     ff1 = js.sf.radial3DLSF(qxzw.reshape(3, -1).T, sclattice, domainsize=ds, rmsd=0.03, hklmax=7)
     ffs1 = ff1.Y # np.log(ff1.Y)
     fmax, fmin = ffs1.max(), ffs1.min()
     ff1Y = (np.reshape(ffs1, xzw[0].shape) - fmin) / (fmax - fmin)
     ax.plot_surface(qxzw[0], qxzw[1], qxzw[2], rstride=1, cstride=1, facecolors=cm.gist_ncar(ff1Y), alpha=0.3)

     qxzw = np.stack([xzw[0]+8, np.zeros_like(xzw[0])+8,  xzw[1]], axis=0)
     ff2 = js.sf.radial3DLSF(qxzw.reshape(3, -1).T, sclattice, domainsize=ds, rmsd=0.03, hklmax=7)
     ffs2 = ff2.Y #np.log(ff2.Y)
     fmax, fmin = ffs2.max(), ffs2.min()
     ff2Y = (np.reshape(ffs2, xzw[0].shape) - fmin) / (fmax - fmin)
     ax.plot_surface(qxzw[0], qxzw[1], qxzw[2], rstride=1, cstride=1, facecolors=cm.gray(ff2Y), alpha=0.3)

     ax.set_xlabel('x axis')
     ax.set_ylabel('y axis')
     ax.set_zlabel('z axis')
     fig.suptitle('Scattering planes of simple cubic lattice \nin powder average')
     pyplot.show(block=False)



    References
    ----------
    .. [1] Scattering curves of ordered mesoscopic materials.
           Förster, S. et al. J. Phys. Chem. B 109, 1347–1360 (2005).
    .. [2] Patterson, A.
           The Scherrer Formula for X-Ray Particle Size Determination
           Phys. Rev. 56 (10): 978–982 (1939)
           doi:10.1103/PhysRev.56.978.
    .. [3] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).1
    """

    qr = np.linalg.norm(qxyz, axis=1)
    qx = np.r_[0:np.max(qr):1j * 2 * np.mean(qxyz.shape) ** 0.5]
    # radial lSF
    lsf = latticeStructureFactor(q=qx, lattice=lattice, domainsize=domainsize, asym=asym, lg=lg, rmsd=rmsd,
                                 beta=beta, hklmax=hklmax, c=c, wavelength=wavelength, corrections=corrections)

    # prepare result for 3D
    result = dA(np.c_[qxyz, lsf.interp(qr)].T)
    # copy attributes from lsf
    result.setattr(lsf)
    result.setColumnIndex(ix=0, iz=1, iw=2, iy=3)
    result.modelname = inspect.currentframe().f_code.co_name
    return result


# Bragg peak shape as Gaussian
def _Lhkl(q, center, pWsigma):
    # Gaussian peak at center with width pWsigma
    Lhkl = np.multiply.reduce(np.exp(-0.5 * ((q - center) / pWsigma) ** 2) / pWsigma / np.sqrt(2 * np.pi), axis=1)
    return Lhkl


def _Z0q(qxyz, qpeaks, f2peaks, peakWidthSigma, rotvector, angle=0, ncpu2=0):
    # calculates scattering intensity in direction qhkl as 3d q vectors
    # qpeaks are 3d peak positions
    # f2peaks are peak intensities
    # peakWidthSigma gaussian width
    # rotvector , angle: rotate q by angle around rotvector is the same as rotate crystal
    # ncpu2 parallel cores only used with Fortran (the 2 prevent usage of multiprocessing in pDA)

    # rotate qxyz
    if rotvector is not None and angle != 0:
        # As we rotate here the qhkl instead of the lattice angle gets a minus sign
        R = formel.rotationMatrix(rotvector, -angle)
        rqxyz = np.einsum('ij,kj->ki', R, qxyz)
    else:
        rqxyz = qxyz.copy()
    # calc Z0q
    if useFortran:
        # Z0q = np.c_[[f2 *  fscatter.cloud.lhkl(rqxyz, q, peakWidthSigma)
        #                            for q, f2 in zip(qpeaks, f2peaks) if la.norm(q)>0]].sum(axis=0)
        # 10% faster than above
        qpnorm = la.norm(qpeaks, axis=1)
        Z0q = fscatter.utils.sumlhklgauss(rqxyz, qpeaks[qpnorm > 0, :], peakWidthSigma, f2peaks[qpnorm > 0], ncpu=ncpu2)
    else:
        Z0q = np.c_[[f2 * _Lhkl(rqxyz, q, peakWidthSigma)
                     for q, f2 in zip(qpeaks, f2peaks) if la.norm(q) > 0]].sum(axis=0)
    return Z0q


def orientedLatticeStructureFactor(qxyz, lattice, rotation=None, domainsize=1000, rmsd=0.02, beta=None,
                                   hklmax=3, nGauss=13, ncpu=0, wavelength=None, corrections=[]):
    r"""
    2D structure factor S(q) of an oriented crystal lattice including particle asymmetry, DebyeWaller factor,
    diffusive scattering, domain rotation and domain size.

    To get the full scattering the formfactor needs to be included (See Notes and Examples).
    1-3 dimensional lattice structures with basis containing multiple atoms (see lattice).
    To orient the crystal lattice use lattice methods .rotatehkl2Vector and .rotateAroundhkl

    Parameters
    ----------
    qxyz : array 3xN
        Wavevector array representing a slice/surface in q-space (3D), units 1/A or 1/nm.
        This can describe a detector plane, section of the Ewald sphere or a line in reciprocal space.
    lattice : lattice object
        Lattice object with arbitrary atoms particles in unit cell,
        or predefined lattice from rhombicLattice, bravaisLattice, scLattice,bccLattice,
        fccLattice, diamondLattice, hexLattice, hcpLattice with scattering length of unit cell atoms.
        See lattices for examples.
    rotation : 4x float as [h,k,l,sigma], None
        Average over rotation of the crystal around axis hkl
        with Gaussian distribution of width sigma (units rad) around actual orientation.
    domainsize : float,list, list of directions
        Domainsize of the crystal, units as lattice constant of lattice.
        According to Debye-Scherrer equation :math:`fwhm=2\pi/domainsize` the peak width is determined [2]_.
         - float        : assume same domainsize in all directions.
         - list 3 float : domainsize in directions of latticeVectors.
         - list 4 x 3   : 3 times domainsize in hkl direction as [[size,h,k,l] ,[..],[..] ]
                         [[3,1,1,1],[100,1,-1,0],[100,1,1,-2]]  is thin in 111 direction and others are thick
                         The user should take care that the directions are nearly orthogonal.
    rmsd : float, default=0.02
        Root mean square displacement :math:`<u^2>^{0.5}` determining the Debye Waller factor.
        Units as lattice constant.
    beta : float, None, dataArray
        Asymmetry factor of the formfactor or reduction due to polydispersity.
         - None beta=1, No beta assumed (spherical symmetric formfactor, no polydispersity)
         - dataArray beta explicitly given as dataArray with beta in .Y column.
           Missing values are interpolated.
         - An approximation for polydisperse beta can be found in [1]_ equ.17.
           This can be realized by  beta=js.dA(np.vstack(q,np.exp(-(q*sr*R)**2)))
           with sr as relative standard deviation of gaussian distribution of the size R.
         - See .formfactor for different formfactors which explicit calculation of beta.
    hklmax : int
        Maximum order of the Bragg peaks.
    wavelength : float, default =  None
        Wavelength of the measurement in units nm.
        For Xray Cu K_a it is 0.15406 nm.
    corrections : list, default=[]
        List of corrections to apply, which depend on the measurement type/geometry.
        See :py:func:`~.structurefactor.latticeStructureFactor`
    nGauss : int, default 13
        Number of points in integration over Gaussian for rotation width sigma.
    ncpu : int, optional
        Number of cpus in the pool.
        Set this to 1 if the integrated function uses multiprocessing to avoid errors.
         - not given or 0   -> all cpus are used
         - int>0      min (ncpu, mp.cpu_count)
         - int<0      ncpu not to use


    Returns
    -------
    dataArray
        Columns [qx,qy,qz,Sq,DW,beta,Z0q]
         - q wavevector
         - Sq = S(q) = (1+beta(q)*(Z0(q)-1)*DW(q))*correction structure factor
         - DW(q)     Debye-Waller factor with (1-DW)=diffusive scattering.
         - beta(q)   asymmetry factor of the formfactor.
         - Z0q       lattice factor Z0(q)
        optional
         - correction       [optional] factor polarisation from Thompson scattering
         - theta scattering angle
        Attributes (+ input parameters)
         - .q_hkl    peak positions
         - .hkl      Miller indices
         - .peakFWHM full width half maximum

    Notes
    -----
    - The scattering intensity of a crystal domain is

      .. math:: I(q)={\Delta\rho}^2 n P(q) S(q)

      with
       - :math:`\Delta\rho` scattering length difference between matrix and particles
       - :math:`n` number density (of elementary cells)
       - :math:`P(q)` form factor
       - :math:`S(q)` structure factor :math:`S(q)`
      For inhomogeneous particles we can incorporate :math:`\Delta\rho(r)` in the formfactor :math:`P(q)`
      if this includes the integrated scattering length differences.
    - The structure factor is [1]_ :

      .. math:: S(q)=1+ \beta(q)(Z_0(q)-1)*DW(Q)

      with
       - :math:`\beta(q)=<F(q)>^2/<F(q)^2>` as asymmetry factor [3]_ dependent on the
         scattering amplitude :math:`F(q)` and particle polydispersity
       -  :math:`DW(q)` Debye Waller factor

    - The  lattice factor is [1]_ :

      .. math :: Z_0(q) = \frac{(2\pi)^3}{mv} \sum\limits_{hkl}f_{hkl}^2L_{hkl}(q,g_{hkl})

      with
       - :math:`g_{hkl}`     peak positions
       - :math:`m`           number of particles per unit cell
       - :math:`f_{hkl}`     unit cell structure factor that takes into account symmetry-related extinction rules
       - :math:`v`         volume of the unit cell
       - :math:`hkl`         reflections

    - Unit cell structure factors :math:`f_{hkl}` are normalised that the lattice factor is normalised for
      infinite q to 1. With i as unit cell atoms at fractional position in the unit cell :math:`[x_i,y_i,z_i]`
      and scattering amplitude :math:`b_i` we get :

      .. math:: f_{hkl}^2 = \big(\sum_i b_i e^{-2\pi (hx_i+ky_i+lz_i)}\big)^2 / \sum_i b_i^2


    - The peak shape function is

      .. math :: L_{hkl}(q,g_{hkl}) = \frac{1}{ \sqrt{2\pi} \sigma} e^{-\frac{(q-g_{hkl})^2}{2\sigma^2}}

      with :math:`\sigma=fwhm/2\sqrt{2log(2)}` related to the domainsize.

      Correspondingly :math:`\sigma` is a vector describing the peak shapes in all directions.

    - Distributions of domain orientation are included by the parameter rotation that describes
      gaussian distributions with mean and sigma around an axis defined by the corresponding hkl indices.

    - DW is a Debye Waller like factor as :math:`DW(q)=e^{-q^2<u^2>}` leading to a reduction
      of scattered intensity and diffusive scattering.
      It has contributions from thermal lattice disorder
      ( DW factor with 1/3 factor in 3D).

    - To get the scattering of a specific particle shape the formfactor has to be included.
      The above is valid for isotropic scatterers (symmetric or uncorrelated to the crystal orientation)
      as only in this case we can separate structure factor and form factor.

    Examples
    --------
    Comparison fcc and sc to demonstrate selection rules ::

     import jscatter as js
     import numpy as np
     R=8
     N=50
     ds=10
     fcclattice= js.lattice.fccLattice(3.1, 5)
     qxy=np.mgrid[-R:R:N*1j, -R:R:N*1j].reshape(2,-1).T
     qxyz=np.c_[qxy,np.zeros(qxy.shape[0])].T
     fcclattice.rotatehkl2Vector([1,1,1],[0,0,1])
     ffe=js.sf.orientedLatticeStructureFactor(qxyz,fcclattice,domainsize=ds,rmsd=0.1,hklmax=4)
     fig=js.mpl.surface(ffe.X,ffe.Z,ffe.Y)
     sclattice= js.lattice.scLattice(3.1, 5)
     sclattice.rotatehkl2Vector([1,1,1],[0,0,1])
     ffs=js.sf.orientedLatticeStructureFactor(qxyz,sclattice,domainsize=ds,rmsd=0.1,hklmax=4)
     fig=js.mpl.surface(ffs.X,ffs.Z,ffs.Y)



    Comparison of different domainsizes dependent on direction of scattering ::

     import jscatter as js
     import numpy as np
     R=8
     N=50
     qxy=np.mgrid[-R:R:N*1j, -R:R:N*1j].reshape(2,-1).T
     qxyz=np.c_[qxy,np.zeros(qxy.shape[0])].T
     sclattice= js.lattice.scLattice(2.1, 5)
     sclattice.rotatehkl2Vector([1,0,0],[0,0,1])
     ds=[[20,1,0,0],[5,0,1,0],[5,0,0,1]]
     ffs=js.sf.orientedLatticeStructureFactor(qxyz,sclattice,domainsize=ds,rmsd=0.1,hklmax=2)
     fig=js.mpl.surface(ffs.X,ffs.Z,ffs.Y)
     fig.axes[0].set_title('symmetric peaks: thinner direction perpendicular to scattering plane')
     fig.show()
     sclattice= js.lattice.scLattice(2.1, 5)
     sclattice.rotatehkl2Vector([0,1,0],[0,0,1])
     ffs=js.sf.orientedLatticeStructureFactor(qxyz,sclattice,domainsize=ds,rmsd=0.1,hklmax=2)
     fig2=js.mpl.surface(ffs.X,ffs.Z,ffs.Y)
     fig2.axes[0].set_title('asymmetric peaks: thin direction is parallel to scattering plane')
     fig2.show()

    Rotation along [1,1,1] axis. It looks spiky because of low number of points in xy plane.
    To improve this the user can use more points, which needs longer computing time ::

     import jscatter as js
     import numpy as np
     # make xy grid in q space
     R=8    # maximum
     N=800  # number of points
     ds=15;
     qxy=np.mgrid[-R:R:N*1j, -R:R:N*1j].reshape(2,-1).T
     # add z=0 component
     qxyz=np.c_[qxy,np.zeros(qxy.shape[0])].T # as position vectors
     # create sc lattice which includes reciprocal lattice vectors and methods to get peak positions
     sclattice= js.lattice.scLattice(2.1, 5)
     # Orient 111 direction perpendicular to qxy plane
     sclattice.rotatehkl2Vector([1,1,1],[0,0,1])
     # rotation by 15 degrees to be aligned to xy plane
     sclattice.rotateAroundhkl([1,1,1],np.deg2rad(15))
     ffs=js.sf.orientedLatticeStructureFactor(qxyz,sclattice, rotation=[1,1,1,np.deg2rad(10)],
                                             domainsize=ds,rmsd=0.1,hklmax=2,nGauss=23)
     fig=js.mpl.surface(ffs.X,ffs.Z,ffs.Y)
     #fig.savefig(js.examples.imagepath+'/orientedlatticeStructureFactor.jpg')

    .. image:: ../../examples/images/orientedlatticeStructureFactor.jpg
     :align: center
     :height: 300px
     :alt: orientedlatticeStructureFactor


    References
    ----------
    .. [1] Order  causes  secondary  Bragg  peaks  in soft  materials
           Förster et al Nature Materials doi: 10.1038/nmat1995
    .. [2] Patterson, A.
           The Scherrer Formula for X-Ray Particle Size Determination
           Phys. Rev. 56 (10): 978–982 (1939)
           doi:10.1103/PhysRev.56.978.
    .. [3] M. Kotlarchyk and S.-H. Chen, J. Chem. Phys. 79, 2461 (1983).1

    """
    if corrections == 'all' or 'all' in corrections:
        corrections = ['TP', 'lh', 'LC', 'area']

    # check that qxyz is in 3xN shape
    if qxyz.shape[1] == 3 and qxyz.shape[0] != 3:
        # transpose
        qxyz = qxyz.T


    vd = lattice.unitCellVolume
    n = len(lattice.unitCellAtoms)
    dim = 3  # dimensionality

    # peakWidthSigma describes Bragg peak width as 3D vector relative to lattice
    if isinstance(domainsize, numbers.Number):
        domainsize = np.array([domainsize] * 3)
        fwhm = 2 * np.pi / np.abs(domainsize)
        peakWidthSigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
    elif isinstance(domainsize, list):
        if np.ndim(domainsize) == 1:
            # use latticevector direction
            domainsize = np.atleast_1d(domainsize)
            # broadening due to domainsize in direction of latticeVectors
            fwhm = 2 * np.pi / np.abs(domainsize)
            sigma = fwhm / (2 * np.sqrt(2 * np.log(2)))
            peakWidthSigma = np.abs(
                np.sum([s * lV / la.norm(lV) for lV, s in zip(lattice.latticeVectors, sigma)], axis=1))
        else:
            # we assume that width with Miller indices is given
            ds = np.array(domainsize)
            sigma = 2 * np.pi / np.abs(ds[:, 0]) / (2 * np.sqrt(2 * np.log(2)))  # width as sigma
            # transform hkl to real directions by using the latticeVectors
            hkldirection = np.einsum('ij,lj', lattice.latticeVectors, ds[:, 1:4])
            peakWidthSigma = np.abs(np.sum([s * lV / la.norm(lV) for lV, s in zip(hkldirection, sigma)], axis=1))
    else:
        raise TypeError('domainsize cannot be interpreted.')

    if rotation is not None:
        # rotation direction
        rotvector = lattice.vectorhkl(rotation[:3])
    else:
        rotvector = None

    # Debye Waller factor
    qr = la.norm(qxyz, axis=0)
    DW = np.exp(-qr ** 2 * rmsd ** 2)

    # reciprocal lattice
    peaks = lattice.getReciprocalLattice(hklmax)
    qpeaks = peaks[:, :3]  # positions
    f2peaks = peaks[:, 3]  # scattering intensity
    hkl = peaks[:, 4:]  # hkl indices

    if rotation is not None and abs(rotation[3]) > 0:
        # gauss distribution of rotation angle
        Z0q = formel.parDistributedAverage(_Z0q, abs(rotation[3]), parname='angle', nGauss=nGauss,
                                           qxyz=qxyz.T, qpeaks=qpeaks, f2peaks=f2peaks,
                                           peakWidthSigma=peakWidthSigma, rotvector=rotvector, angle=0, ncpu2=ncpu)
    else:
        # single orientation
        Z0q = _Z0q(qxyz=qxyz.T, qpeaks=qpeaks, f2peaks=f2peaks,
                   peakWidthSigma=peakWidthSigma, rotvector=rotvector, angle=0, ncpu2=ncpu)
    Z0q *= (2 * np.pi) ** dim / n / vd

    # normalisation
    Z0q = Z0q / np.sum(np.r_[lattice.unitCellAtoms_b]**2)

    if beta is None:
        beta = np.ones_like(qr)
    elif hasattr(beta, '_isdataArray'):
        beta = beta.interp(qr)

    # structure factor
    Sq = 1 + beta * (Z0q - 1) * DW

    if wavelength is None:
        # prepare result
        result = dA(np.vstack([qxyz, Sq, DW, beta, Z0q]))
        result.columnname = 'qx; qy; qz; Sq; DW; beta; Z0q'
    else:
        theta = 2 * np.arcsin(qr * wavelength / 4. / np.pi)
        # Thompson polarisation for electromagnetic scattering
        # https://en.wikipedia.org/wiki/Thomson_scattering
        correction = np.ones_like(Sq)
        if 'TP' in corrections:
            correction = correction * (1 + np.cos(theta) ** 2) / 2
        if 'LC' in corrections:
            correction = correction / np.sin(theta)
        if 'area' in corrections:
            correction = correction / np.sin(theta)
        if 'lh' in corrections:
            correction = correction / np.cos(theta / 2)
        # prepare result
        result = dA(np.vstack([qxyz, Sq * correction, DW, beta, Z0q, correction, theta]))
        result.columnname = 'qx; qy; qz; Sq; DW; beta; Z0q; correction; theta'

    # prepare result
    result.setColumnIndex(iey=None, ix=0, iz=1, iw=2, iy=3)
    result.q_hkl = qpeaks
    result.hkl = hkl
    result.sumfi2 = np.sum(np.r_[lattice.unitCellAtoms_b] ** 2)
    result.peaksigma = peakWidthSigma
    result.domainsize = domainsize
    result.rmsd = rmsd
    result.rotation = rotation
    result.modelname = inspect.currentframe().f_code.co_name
    return result


# noinspection PyIncorrectDocstring
def radialorientedLSF(*args, **kwargs):
    """
    Radial averaged structure factor S(q) of an oriented crystal lattice calculated as orientedLatticeStructureFactor.

    For a detailed description and parameters see orientedLatticeStructureFactor.
    Additionally the qxyz plane according to orientedLatticeStructureFactor is radial averaged over qxyz.

    Parameters
    ----------
    q : int, array
        Explicit list of q values or number of points between min and max wavevector values
        To large number results in noisy data as the average gets artificial.
        Each q points will be averaged in intervals around q neighbors from values in qxyz plane.

    Returns
    -------
    dataArray
        Columns [q,Sq,DW,beta,Z0q]
         - q wavevector as norm(qx,qy,qz)
         - Sq = S(q) = 1+beta(q)*(Z0(q)-1)*DW(q) structure factor
         - DW(q)     Debye-Waller factor with (1-DW)=diffusive scattering.
         - beta(q)   asymmetry factor of the formfactor.
         - Z0q       lattice factor Z0(q)
        Attributes (+ input parameters)
         - .q_hkl    peak positions
         - .hkl      Miller indices
         - .peakFWHM full width half maximum

    Notes
    -----
    qxyz might be any number and geometrical distribution as plane or 3D cube.
    3D qxyz points will be converted to qr=norm(qxyz) and averaged.


    Examples
    --------
    ::

     import jscatter as js
     import numpy as np

     R=12
     N=200
     ds=10
     fcclattice= js.lattice.fccLattice(3.1, 5)
     qxy=np.mgrid[-R:R:N*1j, -R:R:N*1j].reshape(2,-1).T
     qxyz=np.c_[qxy,np.zeros(N**2)].T
     q=np.r_[0.1:16:100j]
     p=js.grace()
     for rmsd in [0.07,0.03,0.01]:
         ffe=js.sf.radialorientedLSF(q=q,qxyz=qxyz,lattice=fcclattice,rotation=[1,1,1,np.deg2rad(10)],domainsize=ds,rmsd=rmsd,hklmax=6)
         p.plot(ffe,li=1,le=f'rmsd {rmsd}')
     p.legend(x=8,y=1.8)
     p.yaxis(label='S(Q)',min=0,max=2.2)
     p.xaxis(label='Q / nm\S-1')
     #p.save(js.examples.imagepath+'/radialorientedLSF.jpg')

    .. image:: ../../examples/images/radialorientedLSF.jpg
     :width: 50 %
     :align: center
     :alt: radialorientedLSF



    """
    # get q values or number of values
    q = kwargs.pop('q', kwargs['qxyz'].shape[0] ** 0.5 / 2)
    olsf = orientedLatticeStructureFactor(*args, **kwargs)

    # set X to the value of radial wavevectors
    olsf[0] = np.linalg.norm(olsf[[olsf._ix, olsf._iz, olsf._iw]], axis=0)
    # cut z and w columns
    radial = olsf[[0, 3, 4, 5, 6]]
    radial.setColumnIndex(ix=0, iy=1, iey=None, iz=None, iw=None)
    radial.isort()  # sorts along X by default
    if isinstance(q, numbers.Number):
        # return lower number of points from prune
        result = radial.prune(number=int(q), type='mean')
    else:
        # explicit given list of q values
        result = radial.prune(kind=q, type='mean', fillvalue = 0.)
        # force exact same Q values ignoring statistical mean
        result.X = q
    result.modelname = inspect.currentframe().f_code.co_name
    return result


# ------------------------------------------------------------------
# hydrodynamic function
# see Beenakker ref 2 Table 1, given is phi*gamma0^m/n
_tablegamma0 = '0.0 0.0 0.0 0.0 0.0 \
              0.05 0.0553 0.0542 0.0533 0.0525 0.10 0.1228 0.1177 0.1135 0.1104 0.15 0.2048 0.1918 0.1813 0.1738  \
              0.20 0.3038 0.2777 0.2574 0.2432 0.25 0.4224 0.3766 0.3423 0.3186 0.30 0.5627 0.4895 0.4364 0.4005  \
              0.35 0.7267 0.6172 0.5402 0.4888 0.40 0.9157 0.7601 0.6538 0.5839 0.45 1.1310 0.9183 0.7776 0.6856'
_gamma0 = np.fromstring(_tablegamma0, sep=' ').reshape(-1, 5).T
# interpolate polynom order 3
_gamma0poly = np.polyfit(_gamma0[0], _gamma0[1:].T, 4)  # about 200µs


# calc values as np.polyval(_gamma0poly,xx)

def _Sg(xx, mm1):
    """
    from Genz [1] equ 6 with gamma0 from [2]_ Table 1
    Sg=C(x) + .......
    this is for all ak (see Beenakker ref 2 ) and accurate in (volume fraction)**2
    returns array
    """
    x = np.where(xx == 0, np.ones_like(xx) * 1e-5, xx)  # avoid zero
    x2 = 2 * x
    x3 = x * x * x
    x4 = x3 * x
    cxx = 9 / 2. * (special.sici(x2)[0] / x + 0.5 * np.cos(x2) / x / x + 0.25 * np.sin(x2) / x3 -
                    np.sin(x) ** 2 / x4 - 4 / x3 / x3 * (np.sin(x) - x * np.cos(x)) ** 2)
    Cx = np.where(xx == 0, np.ones_like(xx) * 2.5, cxx)  # zero is equal 2.5
    func = (Cx + 9. / 4 * np.pi * 5 / 9. * mm1[0] * 9. / x3 * special.jn(1.5, x) ** 2 +
            9. / 4 * np.pi * 1. * mm1[1] * 25. / x3 * special.jn(2.5, x) ** 2 +
            9. / 4 * np.pi * 1. * mm1[2] * 49. / x3 * special.jn(3.5, x) ** 2 +
            9. / 4 * np.pi * 1. * mm1[3] * 81. / x3 * special.jn(4.5, x) ** 2)
    return func


def _HINTEGRAL(Q, Rh, molarity, sffunc, sfargs=None, numberOfPoints=50):
    """
    calculation of hydrodynamic function for one Q
    see hydrodynamicFunct
    """
    # set to zero to get debug messages; debuglevel>10 no messages
    if sfargs is None:
        sfargs = {}
    phi = 4 / 3 * np.pi * Rh ** 3 * constants.N_A * molarity * 1e-24
    if phi > 0.5:
        print('to large volume fraction %.3g in H' % phi)
        return -1
    # coefficients for the gamma0^m/n
    mm1 = np.polyval(_gamma0poly, phi) / phi - 1

    def Sq(q):
        """structure factor; infinite S(Q=inf)=1            """
        # ravel q
        sf = sffunc(q.ravel(), **sfargs)
        # reshape sf to q shape
        if sf._isdataArray: return sf.Y.reshape(q.shape)
        return sf.reshape(q.shape)

    ak = np.r_[0:np.pi * 3:numberOfPoints * 3j, np.pi * 2:np.pi * 53:numberOfPoints * 4j]
    k = ak / Rh
    x = np.cos(np.r_[np.pi:0:-numberOfPoints * 2j])  # x is cos(angle(k,k`))

    Qmk = np.sqrt(Q ** 2 + k ** 2 - 2 * Q * k * x[:, None])
    # (Sq(Qmk)-1) is correct as compared with [2]_ equ 5.7 and 5.9
    integrand = np.sinc(ak / np.pi) ** 2 / (1 + phi * _Sg(ak, mm1)) * (1 - x[:, None] ** 2) * (Sq(Qmk) - 1)
    integrandak = np.trapz(integrand, x=x, axis=0)
    integral = np.trapz(integrandak, x=ak, axis=0)
    return np.r_[Q, 3. / 2. / np.pi * integral]


def _HINTEGRALDs(Rh, molarity, numberOfPoints=50):
    """
    calculation of hydrodynamic function for the self diffusion Ds
    see hydrodynamicFunct
    number of points is number of points in integration in a pi interval
    """
    # set to zero to get debug messages; debuglevel>10 no messages
    phi = 4. / 3 * np.pi * Rh ** 3 * constants.N_A * molarity * 1e-24
    if phi > 0.5:
        print('to large volume fraction %.3g in Ds' % phi)
        return -1
    # coefficients for the gamma0^m/n
    mm1 = np.polyval(_gamma0poly, phi) / phi - 1
    ak = np.r_[0:np.pi * 3:numberOfPoints * 3j, np.pi * 3:np.pi * 153:numberOfPoints * 50j]
    integrandDs = np.sinc(ak / np.pi) ** 2 / (1 + phi * _Sg(ak, mm1))
    integralDs = np.trapz(integrandDs, x=ak)
    return 2 / np.pi * integralDs


def hydrodynamicFunct(wavevector, Rh, molarity, intrinsicVisc=None, DsoverD0=None,
                      structureFactor=None, structureFactorArgs=None,
                      numberOfPoints=50, ncpu=-1):
    r"""
    Hydrodynamic function H(q) from hydrodynamic pair interaction of spheres in suspension.

    This allows the correction :math:`D_T(q)=D_{T0}H(q)/S(q)` for the
    translational diffusion :math:`D_T(q)` coefficient at finite concentration.
    We use the theory from Beenakker and Mazur [2]_ as given by Genz [1]_.
    The :math:`\delta\gamma`-expansion of Beenakker expresses many body hydrodynamic
    interaction within the renormalization approach dependent on the structure factor S(q).

    Parameters
    ----------
    wavevector : array
        scattering vector q in units 1/nm
    Rh : float
        effective hydrodynamic radius of particles in nm.
    molarity : float
        | molarity in mol/l
        | This overrides a parameter 'molarity' in the structureFactorArgs.
        | Rh and molarity define the hydrodynamic interaction, the volume fraction and Ds/D0 for H(Q).
        | The structure factor may have a radius different from Rh e.g. for attenuated hydrodynamic interactions.
    DsoverD0 : float
        | The high Q limit of the hydrodynamic function is for low volume fractions
        | Ds/D0= 1/(1+intrinsicVisc * volumeFraction ) with self diffusion Ds.
        | Ds is calculated from molarity and Rh.
        | This explicit value overrides intrinsic viscosity and calculated Ds/D0.
    structureFactor : function, None
        |  Structure factor S(q) with S(q=inf)=1.0 recommended.
        |  1: If structurefactor is None a Percus-Yevick is assumed with molarity and R=Rh.
        |  2: A function S(q,...) is given as structure factor, which might be an
        |     empirical function (e.g. polynominal fit of a measurement)
        |     First parameter needs to be wavevector q .
        |     If "molarity" parameter is present it is overwritten by molarity above.
    structureFactorArgs : dictionary
        Any extra arguments to structureFactor e.g. structFactorArgs={'x':0.123,R=3,....}
    intrinsicVisc : float
        | Defines the high q limit for the hydrodynamic function.
        | effective_viscosity= eta_solvent * (1-intrinsicVisc*Volumefraction )
        | intrinsicVisc = 2.5 Einstein hard sphere density 1 g/cm**3
        | For proteins instead of volume fraction  the protein concentration in g/ml with typical
        | protein density 1.37 g/cm^3 is often used.
        | Intrinsic Viscosity depends on protein shape (see HYDROPRO).
        | Typical real values for intrinsicVisc in practical units cm^3/g
        |   sphere 1.76 cm^3/g= 2.5    sphere with protein density
        |   ADH    3.9        = 5.5    a tetrameric protein
        |   PGK    4.0        = 5.68   two domains with hinge-> elongated
        |   Rnase  3.2        = 4.54   one domain
        | eta_solvent/effective_viscosity = (1-intrinsicVisc * Volumefraction )=Dself/D0
    numberOfPoints : integer, default 50
        Determines number of integration points in equ 5 of ref [1]_ and therefore accuracy of integration.
        The typical accuracy of this function is <1e-4 for (H(q) -highQLimit) and <1e-3 for Ds/D0.
    ncpu : int, optional
        Number of cpus in the pool.
         - not given or 0   -> all cpus are used
         - int>0      min (ncpu, mp.cpu_count)
         - int<0      ncpu not to use

    Returns
    -------
    dataArray
         Columns [q, HydDynFun, DsoverD0, structureFactor]
          - q values
          - hydrodynamic function
          - hydrodynamic function only Q dependent part = H(q) -highQLimit
          - structure factor for H(q) calculation
          - .selfdiffusion Ds

    Notes
    -----
    Ds is calculated according to equ 11 in [1]_ which is valid for volume fractions up to 0.5.
    With this assumption the deviation of self diffusion Ds from
    Ds=Do*[1-1.73*phi+0.88*phi**2+ O(phi**3)] is smaller 5% for phi<0.2 (10% for phi<0.3)

    References
    ----------
    .. [1] U. Genz and R. Klein, Phys. A Stat. Mech. Its Appl. 171, 26 (1991).
    .. [2] C. W. J. Beenakker and P. Mazur, Phys. A Stat. Mech. Its Appl. 126, 349 (1984).
    .. [3] C. W. J. Beenakker and P. Mazur, Phys. A Stat. Mech. Its Appl. 120, 388 (1983).


    """
    # set to zero to get debug messages; debuglevel>10 no messages
    if structureFactorArgs is None:
        structureFactorArgs = {}
    debuglevel = 0
    if structureFactor is None:
        # we use Percus-Yevick Structure factor --> hard spheres
        structureFactor = PercusYevick
        if 'R' not in structureFactorArgs:
            structureFactorArgs = {'R': Rh}
    sfcode = formel._getFuncCode(structureFactor)
    if 'molarity' in structureFactorArgs or \
            'molarity' in sfcode.co_varnames[:sfcode.co_argcount]:
        # the last examines the function
        # overwrite or append 'molarity'
        structureFactorArgs = dict(structureFactorArgs, **{'molarity': molarity})
    if debug > debuglevel:
        p = grace()
        XX = np.r_[min(wavevector) / 10.:max(wavevector) * 2:100j]
        p.plot(structureFactor(XX, **structureFactorArgs), line=1, symbol=0)
        p.plot(structureFactor(wavevector, **structureFactorArgs))
    # Volume fraction
    phi = lambda mol, R: 4 / 3. * np.pi * R ** 3 * constants.N_A * mol / 10e7 ** 3
    if phi(molarity, Rh) > 0.5:
        raise ValueError(
            'Volume fraction %.3g to high; Chose appropriate Rh or molarity for Volume fraction <0.5' % phi(molarity,
                                                                                                            Rh))
    qqq = np.atleast_1d(wavevector)
    columnname = ['q', 'HydDynFun', 'DsoverD0', 'structureFactor']

    if debug > debuglevel:
        print(columnname[:-1])

        def cb(res):  # for intermediate results
            print(res[0], 1 + res[1], (0 + res[1]))
    else:
        cb = None

    Ds = _HINTEGRALDs(Rh=Rh, molarity=molarity, numberOfPoints=numberOfPoints)
    if DsoverD0 is not None:
        Hinf = DsoverD0
    elif intrinsicVisc is not None:
        DsintrVisc = 1 / (1 + intrinsicVisc * phi(molarity, Rh))
        Hinf = DsintrVisc
        DsoverD0 = DsintrVisc
    else:
        Hinf = Ds
        DsoverD0 = Ds

    # in parallel for production run
    # if debug!= None it will be single thread
    res = parallel.doForQlist(_HINTEGRAL,
                              qqq,
                              Rh=Rh,
                              molarity=molarity,
                              sffunc=structureFactor,
                              sfargs=structureFactorArgs,
                              numberOfPoints=numberOfPoints,
                              ncpu=ncpu,
                              cb=cb, )
    # and calc final result from this
    result = dA(np.c_[qqq,
                      Hinf + np.array(res)[:, 1],
                      np.array(res)[:, 1],
                      structureFactor(wavevector, **structureFactorArgs).Y].T)
    if debug > debuglevel:
        p.plot(result)
    result.Sq = structureFactor
    result.SqArgs = str(structureFactorArgs)
    result.Rh = Rh
    result.molarity = molarity
    result.intrinsicVisc = intrinsicVisc
    result.phi_Rh = phi(molarity, Rh)
    result.DsoverD0 = DsoverD0
    result.numberOfPoints = numberOfPoints
    result.columnname = columnname
    result.setColumnIndex(iey=None)
    return result


def weakPolyelectrolyte(q, cp, l, f, cs, ioc=None, eps=None, Temp=273.15 + 20, contrast=None, molarVolume=None):
    r"""
    Monomer-monomer structure factor S(q) of a weak polyelectrolyte according to Borue and Erukhimovich [3]_.

    Polyelectrolyte models based on [3]_  are valid above "the critical concentration when electrostatic
    blobs begin to overlap", see equ. 2 in [3]_ and above where we dont see isolated chains.
    The used RPA is valid only at high polymer concentrations where concentration fluctuations are weak [4]_.

    Parameters
    ----------
    q : array
        Scattering vector in units 1/nm.
    cp : float
        Monomer concentration :math:`c_p` in units mol/l.
        The monomer concentration is :math:`N c_{p}.
    l : float
        Monomer length in units nm.
    f : float
        Fraction of charged monomers :math:`f`. The abs(f) values is used.
    cs : float
        Monovalent salt concentration :math:`c_s` in the solvent in units mol/l.
        This may include ions from water dissociation.
    ioc : float, default 0
        Additional contribution to the inverse osmotic compressibility Dm of neutral polymer
        solution in units :math:`nm^3`.
        Inverse osmotic compressibility is :math:`Dm=1/(Nc)+v+w^2c` (see [2]_)
        The additional contribution is :math:`ioc=v+w^2c` as used in [1]_ and can be positive or negative.
        :math:`v` and :math:`w` are the second and third virial coefficients [1]_.
    eps : float
        Dielectric constant of the solvent to determine the Bjerum length. Default is H2O at given temperature.
        Use formel.dielectricConstant to determine the constant for your water based solvent including salt.
        For H2O at 293.15 K = 80.08  . Added 1M NaCl = 91.08
    Temp : float, default 273.15+20
        Temperature in units Kelvin.
    contrast : float, default None
        Contrast of the polymer :math:`\rho_{monomer}` relative to the solvent as difference of
        scattering length densities in units :math:`nm^{-2}`.
        See Notes for determination of absolute scattering.
        contrast and molarVolume need to be given.
    molarVolume : float, default None
        Molar volume :math:`V_{monomer}` of the polymer in :math:`nm^{3}`.
        See Notes for determination of absolute scattering.
        contrast and molarVolume need to be given.

    Returns
    -------
    dataArray : 2 x N
        Columns [q, Sq]
         - .epsilon
         - .kappa in 1/nm
         - .screeninglength in nm
         - .r0 characteristic screening length without salt in units nm.
         - .c_monomer Monomer concentration in mol/l
         - .c_salt    Salt concentration in mol/l
         - .c_ions    Ion concentration as :math:`2c_s + fc_p` in mol/l
         - .monomerscatteringlength :math:`c = V_{monomer}\rho_{monomer}`.
           If contrast or molarVolume are None then c=1.
        Sq units is 1/nm = 1/(1e-7 cm) = 1e7 1/cm. (multiply by 1e7 to get units 1/cm)


    Notes
    -----
    Borue and Erukhimovich [3]_ describe the polyelectrolyte scattering in reduced variables (see [3]_ equ 39).
    Rewriting this equation expressing the reduced variables s and t in terms of :math:`r_0` yields :

    .. math:: S(q) = c^2 \frac{1}{4\pi l_b f^2} \frac{q^2+\kappa^2}{1+r_0^4(q^2+\kappa^2)(q^2-12hc_p/l^2)}

    with
     - :math:`r_0^2 = \frac{l}{f\sqrt{48c_p\pi l_b} }` characteristic scale of screening without salt
     - :math:`c=V_{monomer}\rho_{monomer}` scattering length monomer.
     - :math:`l_b = e^2/4\pi\epsilon kT \approx 0.7 nm` Bjerum length.
     - :math:`\kappa^2=4\pi l_b (\sum_s{2c_s} + fc_p)` Debye-Hückel **inverse** screening length
       from salt ions and polymer.
     - :math:`h=ioc` Additional contribution to inverse compressibility.
     - :math:`v` and :math:`w` are the second and third virial coefficients between monomers
       :math:`\rightarrow ioc=v+w^2c` [1]_.

    For low salt concentration (:math:`\kappa < r_0`) the peak is expected at :math:`(q^{*2}+\kappa^2)^2 = r_0^{-4}`
    (see [1]_ and [2]_ after euq. 14) and vanishes for :math:`\kappa > r_0` (see [2]_).

    Examples
    --------
    Poly(sodium 4-styrenesulfonate)(PSS-Na) with a bulk density of 0.801 g/mL. Monomer MW = 184 g/mol,
    monomer length 2 C-C bonds = 2 * 0.15 nm
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.01,4,100)

     Vm=184/0.801/6.022140857e+23/1e-21  # partial molar volume of the polymer in nm**3
     c=0.000698-0.000942 # PSS in H2O for X-ray scattering has negative contrast
     p=js.grace(1.2,1)
     for i,cp in enumerate([5, 10, 20, 30, 60],1): # conc in g/l
        c17=cp/184 # conc in mol/l
        Sq=js.sf.weakPolyelectrolyte(q=q, l=0.3, cp=c17, f=0.05, cs=0.005,ioc=0,contrast=c,molarVolume=Vm)
        Sq.Y*=1e7  # conversion to 1/cm
        p.plot(Sq,sy=[i,0.4,i],li=0,le='c={0:.3} mg/ml'.format(c17))
        Sqi=js.sf.weakPolyelectrolyte(q=q, l=0.3, cp=c17, f=0.05, cs=0.005,ioc=-0.02,contrast=c,molarVolume=Vm)
        Sqi.Y*=1e7
        p.plot(Sqi,li=[1,1,i],sy=0,le='ioc=-0.02 c={0:.3} mg/ml'.format(c17))

     p.yaxis(scale='log',min=Sq.Y.min()/15,max=Sq.Y.max(),label='I(q) / 1/cm')
     p.xaxis(scale='log',min=0.01,max=4,label=r'q / nm\S-1')
     p.title('A polyelectrolyte at low salt')
     p.legend(x=0.02,y=1.5e-1)
     #p.save(js.examples.imagepath+'/weakPolyelectrolyte.png')

    .. image:: ../../examples/images/weakPolyelectrolyte.png
     :align: center
     :height: 300px
     :alt: weakPolyelectrolyte

    References
    ----------

    .. [1] Annealed and quenched polyelectrolytes.
           Raphael, E., & Joanny, J. F. (1990).
           EPL, 13(7), 623–628. https://doi.org/10.1209/0295-5075/13/7/009
    .. [2] Weakly charged polyelectrolytes in a poor solvent
           J.F. Joanny, L. Leibler
           J. Phys. France 51, 545-557 (1990) DOI: 10.1051/jphys:01990005106054500
    .. [3] A statistical theory of weakly charged polyelectrolytes: fluctuations,
           equation of state and microphase separation
           V. Yu. Borue, I. Ya. Erukhimovich, Macromolecules (1988) 21, 11, 3240-3249
    .. [4] 50th Anniversary Perspective: A Perspective on Polyelectrolyte Solutions
           M. Muthukumar
           Macromolecules201750249528-9560
           See p 9537 Pitfall of RPA for Polyelectrolyte solution


    """
    result = dA(np.c_[q, q].T)
    # add attributes in units mol/l
    result.c_salt = cs
    result.c_monomer = cp
    result.c_ions = 2 * cs + cp * abs(f)

    # unit conversion to nm
    # ion concentration for monovalent salt concentration in 1/nm**3 accounting for ion and counter ion
    cs = cs * constants.N_A / 1e24
    # monomer concentration in 1/nm**3
    cp = cp * constants.N_A / 1e24
    if eps is None:
        eps = formel.dielectricConstant('h2o', T=Temp)
    if ioc is None:
        ioc = 0  # -l**3*(-0.1)

    # Bjerrum length in units nm as about 0.7 nm.
    lb = constants.e ** 2 / (4 * np.pi * eps * constants.epsilon_0 * Temp * constants.Boltzmann) * 1e9
    # squared inverse screening length kappa from Debye-Hückel
    k2 = 4 * np.pi * lb * (2 * cs + cp * f)
    q2 = q ** 2
    # characteristic scale of screening squared
    r02 = l / f / (cp * 48 * np.pi * lb) ** 0.5

    # monomer monomer structure factor S(q)
    result.Y = (q2 + k2) / (4 * np.pi * lb * abs(f) ** 2) / (1 + r02 * r02 * (q2 + k2) * (q2 - 12 * ioc * cp / l ** 2))

    if contrast is not None and molarVolume is not None:
        # scale to get absolute scattering
        c = molarVolume * contrast
        result.Y = c ** 2 * result.Y
        result.monomerscatteringlength = c

    result.setColumnIndex(iey=None)
    result.columnname = 'q; Sq'
    result.epsilon = eps
    result.kappa = k2 ** 0.5
    result.screeninglength = 1 / result.kappa
    result.r0 = r02 ** 0.5
    result.modelname = inspect.currentframe().f_code.co_name

    return result


def fractal(q, clustersize, particlesize, df=2):
    r"""
    Structure factor of a fractal cluster of particles following Teixeira (mass fractal).

    To include the shape/structure of a particle with formfactor F(q) use S(q)*F(q) with
    particlesize related to the specific formfactor.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm.
    clustersize : float
        Clustersize :math:`\xi` in units nm. May be correlated to Rg (see Notes).
        From [1]_:
        The meaning of :math:`\xi` is only qualitative and has to be made precise in any particular
        situation. Generally speaking, it represents the characteristic distance above which the mass distribution
        in the sample is no longer described by the fractal law.
        *In practice, it can represent the size of an aggregate or a correlation length in a disordered material.*
    particlesize : float
        Particle size in units nm. In [1]_ it is described as characteristic dimension of individual scatterers.
        See Notes.
    df : float, default=2
        Hausdorff dimension, :math:`d_f` defined as the exponent of the linear dimension R in the
        relation :math:`M(R) \propto (R/r_0)^{d_f}` where M represents the mass and :math:`r_0`
        is the gauge of measurement. See [1]_.

    Returns
    --------
    dataArray : [q, Sq]
        input parameters as attributes
         - .Rg :math:`Rg = d_f(d_f+1) \xi^2/2`  See [1]_ after equ. 17
         - .Sq0  :math:`S(q=0) = 1 + (\xi/r_0)^{d_f}  \Gamma(d_f+1)` see [1]_ equ. 17

    Notes
    -----
    - The structure factor [1]_ equ 16 is

      .. math ::     S(q) = 1 + \frac{d_f\  \Gamma\!(d_f-1)}{[1+1/(q \xi)^2\  ]^{(d_f -1)/2}}
                     \frac{\sin[(d_f-1) \tan^{-1}(q \xi) ]}{(q R_0)^{d_f}}

    - At large q the unity term becomes dominant and we get :math:`S(q)=1`.
      Accordingly the formfactor of the particles becomes visible.
    - At intermediate q :math:`\xi^{-1} < q < r_0^{-1}` the structure factor reduces to :math:`S(q)=q^{-d_f}`

    - The radius of gyration is related to the cluster size :math:`\xi` as
      :math:`Rg = d_f(d_f+1) \xi^2/2`  See [1]_ after equ. 17.

    - According to [1]_ the particlesize relates to a characteristic dimension of the particles.
      The particlesize determines the intersection of the extrapolated power law region with 1 thus
      the region where the particle structure gets important.
      The particlesize can be something like the radius of gyration of a Gaussian or collapsed chain,
      a sphere radius or the mean radius of a protein.
      It might also be the clustersize of a fractal particle.

    - In SASview the particlesize is related to the radius of aggregating spheres (or core shell sphere)
      including a respective formfactor.


    Examples
    --------
    Here a fractal structure of a cluster of spheres is shown.
    The size of the spheres is the particlesize on the cluster.
    The typical scheme :math:`I(q)=P(q)S(Q)` with particle formfactor :math:`P(q)` and structure factor :math:`S(Q)`
    is used. The volume and contrast is included in :math:`P(q)`.
    Add a background if needed or use a different particle as core-shell sphere.
    ::

     import jscatter as js
     import numpy as np
     q=js.loglist(0.01,5,300)

     p=js.grace(1.5,1)
     p.multi(1,2)
     clustersize = 20
     particlesize = 2

     fq=js.ff.sphere(q,particlesize)
     for df in np.r_[0:3:7j]:
         Sq=js.sf.fractal(q, clustersize, particlesize, df=df)
         p[0].plot(Sq,le=f'df={df:.2f}')
         p[1].plot(Sq.X,Sq.Y*fq.Y,li=-1,le=f'df={df:.2f}')

     p[0].yaxis(scale='log',label='I(q) ',min=0.1,max=1e4)
     p[0].xaxis(scale='log',min=0.01,max=4,label='q / nm\S-1')
     p[0].title(r'Fractal structure factor')
     p[0].subtitle('df is fractal dimension')
     p[0].legend(x=0.5,y=1000)
     p[1].yaxis(scale='log',min=0.1,max=1e8,label=['I(q)',1.0,'opposite'],ticklabel=['power',0,1,'opposite'])
     p[1].xaxis(scale='log',min=0.01,max=4,label='q / nm\S-1')
     p[1].title(r'Fractal structure factor of spheres')
     p[1].subtitle('sphere formfactor is added')
     p[1].legend(x=0.5,y=1e7)
     #p.save(js.examples.imagepath+'/fractalspherecluster.png')

    .. image:: ../../examples/images/fractalspherecluster.png
     :align: center
     :height: 300px
     :alt: fractalspherecluster


    References
    ----------
    .. [1] Small-Angle Scattering by Fractal Systems
           J. Teixeira, J. Appl. Cryst. (1988). 21,781-785


    """
    q = np.array(q)
    gamma = special.gamma
    xi = clustersize
    r0 = particlesize
    qxi = q * xi
    Sq = np.zeros_like(q)
    # catch gamma divergence at 0 and 1
    if df == 0:
        Sq = np.ones_like(q)
    else:
        if df == 1:
            Sq[q > 0] = 1 + np.arctan(qxi[q > 0]) / (q[q > 0] * r0)
        else:
            Sq[q > 0] = 1 + df * gamma(df - 1) / (1 + 1 / qxi[q > 0] ** 2) ** ((df - 1) / 2.) * \
                        np.sin((df - 1) * np.arctan(qxi[q > 0])) / (q[q > 0] * r0) ** df
        Sq[q == 0] = 1 + (xi / r0) ** df * gamma(df + 1)

    result = dA(np.c_[q, Sq].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Sq'
    result.modelname = inspect.currentframe().f_code.co_name
    result.clustersize = clustersize
    result.particlesize = particlesize
    result.fractaldimension = df
    result.Rg = df * (df + 1) * xi ** 2 / 2
    result.Sq0 = 1 + (xi / r0) ** df * gamma(df + 1)
    return result


def twoYukawa(q, R, K1, K2, scl1, scl2, molarity=None, phi=None):
    r"""
    Structure factor for a two Yukawa potential in mean spherical approximation.

    A two Yukawa potential in the mean spherical approximation describing cluster formation
    in the two-Yukawa fluid when the interparticle potential is composed of a short-range attraction
    and a long-range repulsion according to Liu et al [1]_.

    Parameters
    ----------
    q : array
        Wavevectors in units 1/nm.
    K1,K2 : float
        Potential strength in units kT.
         - K>1 attraction
         - K<1 repulsion
    scl1,scl2 : float
        Screening length in units nm. The inverse screening length is :math:`Z_i=1/scl_i`.
    R : float
        Radius of the particle in nm.
    phi : float
        Volume fraction of particles in the solution.
    molarity : float
        concentration in units mol/l. Overrides phi if both given.

    Returns
    -------
    dataArray : [q,Sq]
        - additional input attributes
        - On errors in calculation Sq=0 is returned to prevent errors during fitting.
          These are no physical solution.

    Notes
    -----
    The potential is (with :math:`Z_i=1/scl_i`):

    .. math:: \frac{V(r)}{kT} &= \infty   \; &for \; 0<r<1

                             &= -K_1 \frac{e^{-Z_1 (r-1)}}{r} -K_2 \frac{e^{-Z_2 (r-1)}}{r} \; &for \; r>1

    within the MSA closure

    .. math:: h(r) &=-1 \; &for \; 0<r<1

              c(r) &= -\frac{V(r)}{kT} \; &for \; r>1

    - Internally, Z1>Z2 is forced, which is accompanied in the Python code by a swap of K1<>K2 that fitting is smoother.
    - For unphysical or no solution zero is returned.
    - The solution is **unstable close to Z1=Z2**.
      In these cass the (R)MSA structure factor (single Yukawa) is more appropriate.
      The function tries to approximate a solution using K2=>(K1+K2), K1=>0.001K2,Z1=2 Z2


    About the code:
    This Python version of TwoYukawa is based on the code from the IGOR version taken from
    NCNR_SANS_package by Steve Kline (https://github.com/sansigormacros/ncnrsansigormacros)
    The Igor version of this function is based in part on Matlab code supplied by Yun Liu.
    The XOP version of this function is based in part on c-code supplied by Marcus Henning.

    Please cite the paper [1]_, if you use the results produced by this code.

    Examples
    --------

    This reproduces figure 1 in [1]_.
    This figure illustrates the existence of a cluster peak in the structure factor
    for increasing strength K1 of the long-range attraction. ::

     import numpy as np
     import jscatter as js
     q = np.r_[0.01:20:300j]
     R = 0.5
     K2 = -1
     scl1 = 1/10
     scl2 = 1/0.5
     phi =0.2
     #
     p=js.grace(1,0.7)
     for K1 in np.r_[0,3,6,10]:
         Sq = js.sf.twoYukawa(q, R, K1, K2, scl1, scl2, phi=phi)
         p.plot(Sq,li=[1,4,-1],sy=0,le=f'K1={K1:.0f}')
     p.xaxis(label='QD',charsize=2)
     p.yaxis(label='S(Q)',charsize=2)
     p.legend(y=1.95,x=16,charsize=2)
     p.subtitle('S(q) of Two-Yukawa Potential',size=2)
     p.text(r'cluster \npeak',x=2,y=1.9,charsize=2)
     #p.save(js.examples.imagepath+'/twoYukawa.jpg')

    .. image:: ../../examples/images/twoYukawa.jpg
     :width: 50 %
     :align: center
     :alt: ellipsoid

    References
    ----------
    .. [1] Cluster formation in two-Yukawa fluids
           Yun Liu, Wei-Ren Chen, and Sow-Hsin Chen
           THE JOURNAL OF CHEMICAL PHYSICS 122, 044507 (2005) http://dx.doi.org/10.1063/1.1830433

    """
    # get volume fraction phi from number density and radius R
    if isinstance(molarity, numbers.Number):
        molarity = abs(molarity)
        numdens = constants.N_A * molarity * 1e-24  # from mol/l to particles/nm**3
        phi = 4 / 3. * np.pi * R ** 3 * numdens
    elif isinstance(phi, numbers.Number):
        phi = abs(phi)
        numdens = phi / (4 / 3. * np.pi * R ** 3)
        molarity = numdens / (constants.N_A * 1e-24)
    else:
        raise Exception('one of molarity/eta needs to be given.')

    # all details are handled in the Two_Yukawa lib
    Sq = Two_Yukawa.twoYukawa(q, R, K1, K2, 1/scl1, 1/scl2, phi)
    if isinstance(Sq, numbers.Number):
        # On error we return the error code
        return dA(np.c_[q, np.zeros_like(q)].T)
    result = dA(np.c_[q, Sq].T)
    result.setColumnIndex(iey=None)
    result.columnname = 'q; Sq'
    result.R = R
    result.K1 = K1
    result.K2 = K2
    result.scl1 = scl1
    result.scl2 = scl2
    result.phi = phi
    result.molarity = molarity
    result.modelname = inspect.currentframe().f_code.co_name
    return result


