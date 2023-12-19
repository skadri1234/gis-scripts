"""
Shafeeq Kadri
9/23/23
4IND
"""

print("initializing")

from lib5585old import *
import numpy as np

def distance(p_from: list, p_to: list, two_D: True) -> float:
    if two_D:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2) ** 0.5
    else:
        return ((p_to[0] - p_from[0]) ** 2 + (p_to[1] - p_from[1]) ** 2 + (p_to[2] - p_from[2]) ** 2) ** 0.5

def azimuth(p_from: list, p_to: list, converge=0.0) -> float:
    if p_from == p_to:
        print("p_from cant be equal to p_to")
        return None
    az = (np.arctan2(p_to[0]-p_from[0], p_to[1]-p_from[1]) + converge) % twopi
    return az


Y88 = {}
Y88_SPC = {'e': 346299.846, 'n': 261260.194, 'g_DD': 0 + 19/60 + 52.2/3600, 'csf': 0.99997028}

Y88_SPC['g_radians'] = np.deg2rad(Y88_SPC['g_DD'])

Y88['SPC'] = Y88_SPC

Y88_UTM = {'e': 728378.807, 'n': 4632606.690, 'g_DD': 1 + 50/60 + 1.8/3600, 'csf': 1.00021719}

Y88_UTM['g_radians'] = np.deg2rad(Y88_UTM['g_DD'])

Y88['UTM'] = Y88_UTM

STORRS = {}

STORRS_SPC = {'e': 345584.527, 'n': 261520.587, 'g_DD': 0 + 19/60 + 31.6/3600, 'csf': 0.99996451}

STORRS_SPC['g_radians'] = np.deg2rad(STORRS_SPC['g_DD'])

STORRS['SPC'] = STORRS_SPC

STORRS_UTM = {'e': 727656.729, 'n': 4632848.294, 'g_DD': 1 + 49/60 + 41.4/3600, 'csf': 1.00020716}

STORRS_UTM['g_radians'] = np.deg2rad(STORRS_UTM['g_DD'])

STORRS['UTM'] = STORRS_UTM

d_spc = distance([Y88['SPC']['e'], Y88['SPC']['n']],  [STORRS['SPC']['e'], STORRS['SPC']['n']], two_D=True)
d_utm = distance([Y88['UTM']['e'], Y88['UTM']['n']],  [STORRS['UTM']['e'], STORRS['UTM']['n']], two_D=True)

print(f"Grid Distance SPC: {d_spc:.3f}")
print(f"Grid Distance UTM: {d_utm:.3f}")

spc_azimuth = np.rad2deg(azimuth([Y88['SPC']['e'], Y88['SPC']['n']], [STORRS['SPC']['e'], STORRS['SPC']['n']]))
utm_azimuth = np.rad2deg(azimuth([Y88['UTM']['e'], Y88['UTM']['n']], [STORRS['UTM']['e'], STORRS['UTM']['n']]))

print(f"SPC Azimuth: {spc_azimuth:.3f}")
print(f"UTM Azimuth: {utm_azimuth:.3f}")

avg_spc = (Y88['SPC']['csf'] + STORRS['SPC']['csf']) / 2
avg_utm = (Y88['UTM']['csf'] + STORRS['UTM']['csf']) / 2

geodesic_spc = d_spc / avg_spc
print(f"geodesic distance spc: {geodesic_spc:.3f}")
geodesic_utm = d_utm / avg_utm
print(f"geodesic distance utm: {geodesic_utm:.3f}")

avg_convergence_spc = (Y88['SPC']['g_radians'] + STORRS['SPC']['g_radians']) / 2
avg_convergence_utm = (Y88['UTM']['g_radians'] + STORRS['UTM']['g_radians']) / 2

geodetic_azimuth_spc = spc_azimuth + np.rad2deg(avg_convergence_spc)
geodetic_azimuth_utm = utm_azimuth + np.rad2deg(avg_convergence_utm)

print(f"geodetic azimuth spc: {geodetic_azimuth_spc:.4f}")
print(f"geodetic azimuth utm: {geodetic_azimuth_utm:.4f}")

## Repeat the independent assignment from Module 2 below (copy and paste is fine),
## but then doing the distance and azimuth computations using
## your functions you implemented in lib5585, imported above.



