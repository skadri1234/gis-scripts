"""
Shafeeq Kadri
9/4/23
2IND
"""
import numpy as np
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

d_spc = ((Y88['SPC']['e'] - STORRS['SPC']['e'])**2 + (Y88['SPC']['n'] - STORRS['SPC']['n'])**2)**0.5
print(f"grid distance spc: {d_spc:.3f}")
d_utm = ((Y88['UTM']['e'] - STORRS['UTM']['e'])**2 + (Y88['UTM']['n'] - STORRS['UTM']['n'])**2)**0.5
print(f"grid distance utm: {d_utm:.3f}")

avg_spc = (Y88['SPC']['csf'] + STORRS['SPC']['csf']) / 2
# print(avg_spc)
avg_utm = (Y88['UTM']['csf'] + STORRS['UTM']['csf']) / 2
# print(avg_utm)

geodesic_spc = d_spc / avg_spc
print(f"geodesic distance spc: {geodesic_spc:.3f}")
geodesic_utm = d_utm / avg_utm
print(f"geodesic distance utm: {geodesic_utm:.3f}")

spc_e_delta = STORRS['SPC']['e'] - Y88['SPC']['e']
spc_n_delta = STORRS['SPC']['n'] - Y88['SPC']['n']
spc_azimuth = (np.rad2deg(np.arctan2(spc_e_delta, spc_n_delta))) % 360
print(f"spc azimuth: {spc_azimuth:.4f}")
utm_e_delta = STORRS['UTM']['e'] - Y88['UTM']['e']
utm_n_delta = STORRS['UTM']['n'] - Y88['UTM']['n']
utm_azimuth = (np.rad2deg(np.arctan2(utm_e_delta, utm_n_delta))) % 360
print(f"utm azimuth: {utm_azimuth:.4f}")

avg_convergence_spc = (Y88['SPC']['g_DD'] + STORRS['SPC']['g_DD']) / 2
avg_convergence_utm = (Y88['UTM']['g_DD'] + STORRS['UTM']['g_DD']) / 2
geodetic_azimuth_spc = spc_azimuth + avg_convergence_spc
geodetic_azimuth_utm = utm_azimuth + avg_convergence_utm
print(f"geodetic azimuth spc: {geodetic_azimuth_spc:.4f}")
print(f"geodetic azimuth utm: {geodetic_azimuth_utm:.4f}")





