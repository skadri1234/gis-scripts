"""
Various implementations of the direct- and indirect-problems of geodesic lines on the
surface of a reference ellipsoid

Thomas H Meyer
15 Dec 2020
"""
from refellipsoid import *
import numpy as np
from numpy import sqrt, sin, cos, tan, arcsin, arccos, arctan, arctan2, pi

twopi = 2*pi

"""
class Geodesic
Implements geodesics on realistic Earth models: sphere and reference ellipsoids
"""

class Geodesic:
    def __init__(self, RE:refEllipsoid):
        self.RE = RE

    def direct(self, pfrom, s: float, az: float):
        assert False, 'not implemented in base class'

    def direct_parallel(self, pfrom, s: float, az: float):
        """
        The direct problem along the Equator
        :param pfrom: starting point [lon1, lat1]
        :param s: distance to go (m)
        :param az: either pi/2 or -pi/2
        :return: [lon2, lat1]
        """
        return pfrom[0] + s / (cos(pfrom[1]) * self.RE.a)

    def direct_meridian(self, pfrom, s: float, az: float):
        """
        The direct problem along the Equator
        :param pfrom: starting point [lon1, 0]
        :param s: distance to go (m)
        :param az: either pi/2 or -pi/2
        :return: [lon2, 0]
        """
        return pfrom[0] + s / self.RE.a

    def indirect(self, pfrom, pto):
        assert False, 'not implemented in base class'


class sphere(Geodesic):
    def __init__(self, RE:refEllipsoid):
        Geodesic.__init__(self, RE)

    def direct(self, pfrom, s: float, az: float):
        lonA, latA = pfrom[:2]
        R = self.RE.Ra(latA, az)
        c = s / R
        QA = piOn2 - pfrom[1]
        QB = arccos(cos(QA) * cos(c) + sin(QA) * sin(c) * cos(az))
        latB = piOn2 - QB
        lonB = pfrom[0] + s * sin(az) / (self.RE.N(latB) * cos(latB))
        return lonB, latB

    def indirect(self, pfrom, pto):
        latA = pfrom[1]
        QA = piOn2 - latA
        latB = pto[1]
        QB = piOn2 - latB
        dLon = pto[0] - pfrom[0]
        dLat = latB - latA
        sB = sin(dLat/2)
        sB = sB * sB
        sL = sin(dLon/2)
        sL = sL * sL
        c = 2 * arcsin(sqrt(sin(sB) + cos(latA) * cos(latB) * sin(sL)))
        sin_c = sin(c)
        cos_c = cos(c)
        a1f = arccos((cos(QB) - cos(QA) * cos_c) / (sin(QA) * sin_c))
        a2r = (twopi - arccos((cos(QA) - cos(QB) * cos_c) / (sin(QB) * sin_c))) % twopi
        aBar = (a1f + (a2r + pi)%twopi)/2
        R = self.RE.Ra((latA + latB)/2, aBar)
        return c, R * c, a1f, a2r


class bowring81(Geodesic):
    def __init__(self, RE:refEllipsoid):
        Geodesic.__init__(self, RE)
        self.a = RE.a
        self.e = RE.a**2 / RE.b**2 - 1
        self.e_sq = RE.ecc1sq

    def direct(self, pfrom, s: float, az: float):
        L1, B1 = pfrom[:2]
        A = sqrt(1 + self.e * cos(B1) ** 4)
        B = sqrt(1 + self.e * cos(B1) ** 2)
        C = sqrt(1 + self.e)
        sigma = s * B*B / (self.a * C)
        dL = arctan(A * tan(sigma) * sin(az) / (B * cos(B1) - tan(sigma) * sin(B1) * cos(az))) / A
        L2 = L1 + dL
        w = A * dL/2
        D = arcsin(sin(sigma) * (cos(az) - sin(B1) * sin(az) * tan(w) / A)) / 2
        B2 = B1 + 2*D * (B - 3/2 * self.e * D * sin(2*B1 + 4/3 * B * D))
        return [L2, B2]

    def indirect(self, pfrom, pto):
        L1, B1 = pfrom[:2]
        L2, B2 = pto[:2]
        A = sqrt(1 + self.e * cos(B1) ** 4)
        B = sqrt(1 + self.e * cos(B1) ** 2)
        C = sqrt(1 + self.e)
        w = A * (L2 - L1) / 2
        del_lat = B2 - B1
        D = del_lat/(2*B) * (1 + 3*self.e/(4*B**2) * del_lat * sin(2*B1 + (2/3)*del_lat))
        E = sin(D)*cos(w)
        F = sin(w)*(B*cos(B1)*cos(D) - sin(B1)*sin(D)) / A
        G = arctan2(F, E)
        sig = 2.0 * arcsin(sqrt(E*E + F*F))
        H = arctan( (sin(B1) + B * cos(B1) * tan(D)) * tan(w) / A)
        alp1 = (G - H) % (2*pi)
        alp2 = (G + H + pi) % (2*pi)
        s = self.a * C * sig / B**2
        return [s, alp1, alp2]
