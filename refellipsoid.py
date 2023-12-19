"""
refellipsoid

Thomas H Meyer
Department of Natural Resources and the Environment
University of Connecticut
28-June-2019

Reference ellipsoids
"""

import sys
import numpy as np
from numpy import sqrt, sin, cos, pi, arctanh
from mpmath import ellippi
from scipy.optimize import root_scalar, fixed_point
from scipy import integrate
piOn2 = 0.5 * pi
twopi = 2*pi

class EarthModel:
    """
    An earth model is a realistic model of Earth's macroscopic
    shape: spheres and spheroids are the most common
    """
    def __init__(self, a, nm='no name'):
        """
        All reference ellipsoids have two defining parameters that provide
        the size and shape of the spheroid. These defining values are to
        be looked up in an authoritative reference. Some reference ellipsoids
        are defined by the length of the semi-minor axis instead of flattening.

        a: float. The length of the semi-major axis (m).
        nm: str. The name of this ellipsoid.
        sp: float. The value of the shape parameter, either flattening or the
            length of the semi-minor axis (m).
        """
        assert a > 0
        self.name = nm
        self.a = a

    def perimeter(self):
        """
        The Gauss-Kummer relation (Chandrupatla, T.R. and Osler, T.J. (2010) The perimeter of an ellipse.
        In Mathematical Scientist 35, pp. 122-131), p.127
        :param nterms: int = number of terms in the series to evaluate
        :return: float: the perimeter of a meridional ellipse
        """
        pass

    def full(self):
        """
        Return all of this object's attributes as a tuple.
        """
        return self.name, self.a

    def N(self, lat)->float:
        """
        Return the radius of curvature in the prime vertical (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        return self.a

    def M(self, lat)->float:
        """
        Return the radius of curvature in the meridian (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        return self.a

    def NM(self, lat)->tuple:
        """
        Compute N and M which saves some computations
        :param lat:
        :return:
        """
        return self.a, self.a

    def GaussianCurvature(self, lat)->float:
        """
        Return the radius of curvature in the meridian (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        N, M = self.NM(lat)
        GC =  sqrt(N * M)
        return GC

    def Ra(self, lat, az, all=False):
        """
        Return the radius of curvature in the normal sections (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        az: float. Geodetic azimuth (radians). -2 pi <= az <= 2 pi
        """
        pass

    def tsf(self, lbh)->float:
        """
        topographic scale factor on a surface of revolution
        """
        l, b, h = lbh
        return 1 + h / self.GaussianCurvature(b)

    def ns_scale(self, lat:float):
        return 1

    def ew_scale(self, lat:float):
        return 1

    def scales(self, lat:float):
        return 1, 1

    def meridional_indirect(self, phi0:float, phi1:float):
        """
        Return the signed distance along the meridian from lat0 to phi
        :param phi0: float (radians). Starting latitude
        :param phi1: float (radians). ending latitude
        :return: float (meters) arc length of the meridian
        """
        pass

    def meridional_direct(self, phi0:float, s:float):
        """
        Return the geodetic latitude that is <s> meters away of <lat0>
        :param phi0: float (radians). Starting latitude
        :param s: float (meters): distance to go along meridian. Negative value indicate southwards
        :return: float (radians): latitude of forward point
        """
        pass

    def parallel_indirect(self, phi0:float, lon0:float, lon1:float):
        """
        Return the signed distance along the parallel at lat0 from lon0 to lon1
        :param phi0: float (radians). latitude of the parallel
        :param lon0: float (radians). starting longitude
        :param lon1: float (radians). ending longitude
        :return: float (meters) arc length of the parallel
        """
        pass

    def parallel_direct(self, phi0:float, lon0:float, s:float):
        """
        Return the longitude that is <s> meters east/west of <lon0>
        :param phi0: float (radians). Geodetic latitude of the parallel
        :param s: float (meters): distance to go along parallel. Negative value indicate westwards
        :return: float (radians): longitude of forward point
        """
        pass

    def __str__(self):
        return '{} a={:0.3f}'.format(self.name, self.a)

    def __repr__(self):
        return '{} a={:0.3f}'.format(self.name, self.a)


class SphericalEarthModel(EarthModel):
    """
    An earth model is a realistic model of Earth's macroscopic
    shape: spheres and spheroids are the most common
    """
    def __init__(self, a, nm='no name'):
        """
        All reference ellipsoids have two defining parameters that provide
        the size and shape of the spheroid. These defining values are to
        be looked up in an authoritative reference. Some reference ellipsoids
        are defined by the length of the semi-minor axis instead of flattening.

        a: float. The length of the semi-major axis (m).
        nm: str. The name of this ellipsoid.
        sp: float. The value of the shape parameter, either flattening or the
            length of the semi-minor axis (m).
        """
        EarthModel.__init__(self, a, nm=nm)
        self.f = 0
        self.b = a
        self.OneMinusf = 1
        self.ecc1sq = 0
        self.one_minus_ecc1sq = 1.0
        self.a1me2 = self.a
        self.ecc1 = 0
        self.ecc2sq = 0
        self.ecc2 = 0
        aSq = self.a * self.a
        self.mean_radius_IUGG = a
        self.meridional_arc = a * piOn2
        self.mean_M = a
        self.area = 4.0*pi*aSq
        self.volume = 4.0/3.0 * pi * aSq * self.b

    def full(self):
        """
        Return all of this object's attributes as a tuple.
        """
        return self.name, self.a, self.f, self.b, self.ecc1, self.ecc1sq, self.ecc2, self.ecc2sq, self.volume, \
               self.area, self.mean_M, self.mean_radius_IUGG

    def perimeter(self, nterms=10):
        """
        The Gauss-Kummer relation (Chandrupatla, T.R. and Osler, T.J. (2010) The perimeter of an ellipse.
        In Mathematical Scientist 35, pp. 122-131), p.127
        :param nterms: int = number of terms in the series to evaluate
        :return: float: the perimeter of a meridional ellipse
        """
        return 2*pi*self.a

    def w2(self, lat): return 1.0

    def w(self, lat): return 1.0

    def N(self, lat):
        """
        Return the radius of curvature in the prime vertical (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        return self.a

    def M(self, lat):
        """
        Return the radius of curvature in the meridian (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        return self.a

    def NM(self, lat):
        """
        Compute N and M which saves some computations
        :param lat:
        :return:
        """
        return self.a, self.a

    def GaussianCurvature(self, lat):
        """
        Return the radius of curvature in the meridian (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        return self.a

    def Ra(self, lat, az, all=False):
        """
        Return the radius of curvature in the normal sections (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        az: float. Geodetic azimuth (radians). -2 pi <= az <= 2 pi
        """
        return self.a

    def meridional_indirect(self, phi0:float, phi1:float):
        """
        Return the signed distance along the meridian from lat0 to phi
        :param phi0: float (radians). Starting latitude
        :param phi1: float (radians). ending latitude
        :return: float (meters) arc length of the meridian
        """
        assert -piOn2 <= phi0 <= piOn2
        assert -piOn2 <= phi1 <= piOn2
        return self.a * (phi1-phi0)

    def meridional_direct(self, phi0:float, s:float):
        """
        Return the geodetic latitude that is <s> meters away of <lat0>
        :param phi0: float (radians). Starting latitude
        :param s: float (meters): distance to go along meridian. Negative value indicate southwards
        :return: float (radians): latitude of forward point
        """
        assert -piOn2 <= phi0 <= piOn2
        return phi0 + s / self.a

    def parallel_indirect(self, phi0:float, lon0:float, lon1:float):
        """
        Return the signed distance along the parallel at lat0 from lon0 to lon1
        :param phi0: float (radians). latitude of the parallel
        :param lon0: float (radians). starting longitude
        :param lon1: float (radians). ending longitude
        :return: float (meters) arc length of the parallel
        """
        assert -piOn2 <= phi0 <= piOn2
        assert -pi <= lon0 <= pi
        assert -pi <= lon1 <= pi
        return self.a * cos(phi0) * (lon1 - lon0) # d = r theta

    def parallel_direct(self, phi0:float, lon0:float, s:float):
        """
        Return the longitude that is <s> meters east/west of <lon0>
        :param phi0: float (radians). Geodetic latitude of the parallel
        :param s: float (meters): distance to go along parallel. Negative value indicate westwards
        :return: float (radians): longitude of forward point
        """
        assert -piOn2 <= phi0 <= piOn2
        assert -pi <= lon0 <= pi
        return lon0 + s / (self.a * cos(phi0))

    def __str__(self):
        return '{} a={:0.3f}, b={:0.3f}, f={:0.11f}'.format(self.name, self.a, self.a, 0.0)

    def __repr__(self):
        nm, a, f, b, ecc1, ecc1sq, ecc2, ecc2sq, vol, area, mean_M, mean_radius_IUGG = self.full()
        return f'{nm} a={a:0.3f}, vol={vol:0.3f}, area={area:0.3f}'


class refEllipsoid(EarthModel):
    """
    A reference ellipsoid is a spheroidal model of Earth's macroscopic
    shape. The two modern reference ellipsoids are GRS80 and WGS84,
    which are defined here as objects of this class.
    """
    def __init__(self, a:float, sp:float, shapeParameter='flattening', nm='no name'):
        """
        All reference ellipsoids have two defining parameters that provide
        the size and shape of the spheroid. These defining values are to
        be looked up in an authoritative reference. Some reference ellipsoids
        are defined by the length of the semi-minor axis instead of flattening.

        a: float. The length of the semi-major axis (m).
        nm: str. The name of this ellipsoid.
        sp: float. The value of the shape parameter, either flattening or the
            length of the semi-minor axis (m).
        """
        EarthModel.__init__(self, a, nm)
        """
        All reference ellipsoids have two defining parameters that provide
        the size and shape of the spheroid. These defining values are to
        be looked up in an authoritative reference. Some reference ellipsoids
        are defined by the length of the semi-minor axis instead of flattening.

        a: float. The length of the semi-major axis (m).
        nm: str. The name of this ellipsoid.
        sp: float. The value of the shape parameter, either flattening or the
            length of the semi-minor axis (m).
        """
        assert a > 0
        self.name = nm
        self.a = a
        if shapeParameter == 'flattening':
            assert 0 <= sp < 1
            self.f = f = sp
            self.b = a - a * f
        elif shapeParameter == 'semiMinor':
            assert sp <= a
            self.b = b = sp
            self.f = (a - b)/a
        else:
            print("unexpected value for shapeParameter: {0}".format(shapeParameter))
            sys.exit(-1)
        self.OneMinusf = 1 - self.f
        self.ecc1sq = 2 * self.f - self.f*self.f
        self.one_minus_ecc1sq = 1.0 - self.ecc1sq
        self.a1me2 = self.a * self.one_minus_ecc1sq
        self.ecc1 = sqrt(self.ecc1sq)
        self.ecc2sq = (a**2 - self.b**2)/self.b**2
        self.ecc2 = sqrt(self.ecc2sq)
        aSq = self.a * self.a
        self.mean_radius_IUGG = (2 * self.a + self.b) / 3
        self.meridional_arc = integrate.quad(self.M, 0, piOn2)[0]
        self.mean_M = self.meridional_arc / piOn2
        self.area = 2.0*pi*aSq * (1.0 + self.b**2 / (self.ecc1 * aSq) * arctanh(self.ecc1))
        self.volume = 4.0/3.0 * pi * aSq * self.b
        self.h = (self.a - self.b) / (self.a + self.b)  # for the power series for arc length

    def perimeter(self, nterms=10):
        """
        The Gauss-Kummer relation (Chandrupatla, T.R. and Osler, T.J. (2010) The perimeter of an ellipse.
        In Mathematical Scientist 35, pp. 122-131), p.127
        :param nterms: int = number of terms in the series to evaluate
        :return: float: the perimeter of a meridional ellipse
        """
        h = self.h
        hsq = h*h
        num_seq = [1, 1, 1]
        num = 1
        for i in range(2, nterms-1):
            num = num * (2*i - 1)
            num_seq.append(num)
        denom_seq = [1]
        denom = 1
        for i in range(1, nterms):
            denom = denom * 2 * i
            denom_seq.append(denom)
        h = 1
        c = pi * (self.a + self.b)
        total = c
        for i in range(1,nterms):
            t = num_seq[i] / denom_seq[i]
            h = h * hsq
            total += c * t*t * h
        return total

    def w2(self, lat):
        """
        w**2 = 1 - eccSq sinlat**2
        w**2 is a common form in many formulas so it's convenient to have it handy
        :param lat:
        :return:
        """
        assert -pi/2.0 <= lat <= pi/2.0
        sinlat = sin(lat)
        sin2 = sinlat * sinlat
        return 1.0 - self.ecc1sq * sin2

    def w(self, lat): return sqrt(self.w2(lat))

    def N(self, lat):
        """
        Return the radius of curvature in the prime vertical (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        w = self.w(lat)
        value = self.a / w
        return value

    def M(self, lat)->float:
        """
        Return the radius of curvature in the meridian (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        denom = self.w2(lat)**(3/2)
        value =  self.a * self.one_minus_ecc1sq / denom
        return value

    def NM(self, lat):
        """
        Compute N and M which saves some computations
        :param lat:
        :return:
        """
        sinlat = sin(lat)
        sin2 = sinlat * sinlat
        w2 =  1.0 - self.ecc1sq * sin2
        w = sqrt(w2)
        N = self.a / w
        denom = self.w(lat)**(3/2)
        M = self.a * self.one_minus_ecc1sq / denom
        return N, M

    def GaussianCurvature(self, lat):
        """
        Return the radius of curvature in the meridian (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        """
        """
        The classic definition is
        N, M = self.NM(lat)
        GC =  sqrt(N * M)
        but it's faster to do some algebra and evaluate this:
        """
        old = sqrt(self.N(lat) * self.M(lat))
        new = self.b / self.w2(lat)
        return new

    def Ra(self, lat, az, all=False):
        """
        Return the radius of curvature in the normal sections (m).
        lat: float. Geodetic latitude (radians). -pi/2.0 <= lat <= pi/2.0
        az: float. Geodetic azimuth (radians). -2 pi <= az <= 2 pi
        """
        assert -pi / 2.0 <= lat <= pi / 2.0
        assert -2*pi     <= az  <= 2*pi

        N, M = self.NM(lat)
        cosa = cos(az)
        cos2 = cosa * cosa  # avoid a function call
        sin2 = 1.0 - cos2  # avoid lots of stuff
        res = N*M / (N*cos2 + M*sin2)
        if all:
            return res, N, M
        else:
            return res

    def meridional_indirect(self, phi0:float, phi1:float):
        """
        Return the signed distance along the meridian from lat0 to phi
        :param phi0: float (radians). Starting latitude
        :param phi1: float (radians). ending latitude
        :return: float (meters) arc length of the meridian
        """
        assert -piOn2 <= phi0 <= piOn2
        assert -piOn2 <= phi1 <= piOn2
        a = self.a
        ecc1sq = self.ecc1sq
        k1 = a * self.one_minus_ecc1sq
        """
        s0 is the distance from equator to starting latitude
        """
        s0 = k1 * ellippi(ecc1sq, phi0, ecc1sq)
        """
        s1 is the distance from equator to ending latitude
        """
        s1 = k1 * ellippi(ecc1sq, phi1, ecc1sq)
        return float(s1 - s0)

    def meridional_direct(self, phi0:float, s:float):
        """
        Return the geodetic latitude that is <s> meters away of <lat0>
        :param phi0: float (radians). Starting latitude
        :param s: float (meters): distance to go along meridian. Negative value indicate southwards
        :return: float (radians): latitude of forward point
        """
        assert -piOn2 <= phi0 <= piOn2
        a = self.a
        ecc1sq = self.ecc1sq
        k1 = a * self.one_minus_ecc1sq
        """
        s0 is the distance from equator to starting latitude
        """
        s0 = k1 * ellippi(ecc1sq, phi0, ecc1sq)
        """
        Seek ending latitude phi1 st distance from equator to phi1 - d0 == s
        """
        tgt_d = s + s0
        f = lambda phi1: k1 * ellippi(ecc1sq, phi1, ecc1sq) - tgt_d
        if s < 0.0:
            upper_limit = -piOn2
        else:
            upper_limit = piOn2
        sol = root_scalar(f, bracket=[phi0, upper_limit])
        return sol.root

    def parallel_indirect(self, phi0:float, lon0:float, lon1:float):
        """
        Return the signed distance along the parallel at lat0 from lon0 to lon1
        :param phi0: float (radians). latitude of the parallel
        :param lon0: float (radians). starting longitude
        :param lon1: float (radians). ending longitude
        :return: float (meters) arc length of the parallel
        """
        assert -piOn2 <= phi0 <= piOn2
        assert -pi <= lon0 <= pi
        assert -pi <= lon1 <= pi
        R = self.N(phi0) * cos(phi0)
        return R * (lon1 - lon0) # d = r theta

    def parallel_direct(self, phi0:float, lon0:float, s:float):
        """
        Return the longitude that is <s> meters east/west of <lon0>
        :param phi0: float (radians). Geodetic latitude of the parallel
        :param s: float (meters): distance to go along parallel. Negative value indicate westwards
        :return: float (radians): longitude of forward point
        """
        assert -piOn2 <= phi0 <= piOn2
        assert -pi <= lon0 <= pi
        R = self.N(phi0) * cos(phi0)
        return lon0 + s / R

    def full(self):
        """
        Return all of this object's attributes as a tuple.
        """
        return self.name, self.a, self.f, self.b, self.ecc1, self.ecc1sq, self.ecc2, self.ecc2sq, self.volume, \
               self.area, self.mean_M, self.mean_radius_IUGG, self.h

    def __str__(self):
        return '{} a={:0.3f}, b={:0.3f}, 1/f={:0.11f}'.format(self.name, self.a, self.b, 1.0/self.f)

    def __repr__(self):
        nm, a, f, b, ecc1, ecc1sq, ecc2, ecc2sq, vol, area, mean_M, mean_radius_IUGG, h = self.full()
        return f'{nm} a={a:0.3f}, b={b:0.3f}, 1/f={1.0/f:0.11f}, e1={ecc1:0.11f}, e1sq={ecc1sq:0.11f}, ' \
               f'e2={ecc2:0.11f}, e2sq={ecc2sq:0.11f}, vol={vol}, area={area}, mean M={mean_M:0.3f}, ' \
               f'mean R IUGG={mean_radius_IUGG:0.3f}, , mean R IUGG={h:0.3f}'


GRS80 = refEllipsoid(6378137.0, 1.0/298.257222101, nm="GRS80")
WGS84 = refEllipsoid(6378137.0, 1.0/298.257223563, nm='WGS84')
Clarke1866 = refEllipsoid(6378206.4, 6356583.8, shapeParameter='semiMinor', nm='Clarke 1866')
International1924 = refEllipsoid(6378388.0, 1.0/297.0, nm='International 1924')