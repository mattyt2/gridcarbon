# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 20:44:20 2021

@author: Matt
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt



# very approximate
# latitude, longitude, name, altitude, timezone
latitude = 53
longitude = 1
name = 'Norfolk'
altitude = 200
timezone = 'Etc/GMT+0'


import pvlib

# def get_
# get the module and inverter specifications from SAM
sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')

sapm_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')

module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']

inverter = sapm_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']

temperature_model_parameters = pvlib.temperature.TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']

# specify constant ambient air temp and wind for simplicity
temp_air = 20

wind_speed = 0


system = {'module': module, 'inverter': inverter}
naive_times = pd.date_range(start='01/01/2018 00:00', end='12/31/2018 23:00', freq='1h')
# for latitude, longitude, name, altitude, timezone in coordinates:
times = naive_times.tz_localize(timezone)
system['surface_tilt'] = 30
system['surface_azimuth'] = 180
solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude)
dni_extra = pvlib.irradiance.get_extra_radiation(times)
airmass = pvlib.atmosphere.get_relative_airmass(solpos['apparent_zenith'])
pressure = pvlib.atmosphere.alt2pres(altitude)
am_abs = pvlib.atmosphere.get_absolute_airmass(airmass, pressure)
tl = pvlib.clearsky.lookup_linke_turbidity(times, latitude, longitude)
cs = pvlib.clearsky.ineichen(solpos['apparent_zenith'], am_abs, tl,
                             dni_extra=dni_extra, altitude=altitude)
aoi = pvlib.irradiance.aoi(system['surface_tilt'], system['surface_azimuth'],
                           solpos['apparent_zenith'], solpos['azimuth'])
total_irrad = pvlib.irradiance.get_total_irradiance(system['surface_tilt'],
                                                    system['surface_azimuth'],
                                                    solpos['apparent_zenith'],
                                                    solpos['azimuth'],
                                                    cs['dni'], cs['ghi'], cs['dhi'],
                                                    dni_extra=dni_extra,
                                                    model='haydavies')
effective_irradiance = pvlib.pvsystem.sapm_effective_irradiance(
    total_irrad['poa_direct'], total_irrad['poa_diffuse'],
    am_abs, aoi, module)
sunshine = np.asarray(effective_irradiance)


    
yields = np.empty((0,3))




