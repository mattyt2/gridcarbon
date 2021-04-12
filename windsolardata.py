# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 19:54:45 2021

@author: Matt
"""

import requests as rq
import xml.etree.ElementTree as ET
import numpy as np
import matplotlib.pyplot as plt
from datetime import date


APIKey = 'g0t43vms7e1tlk9'
Date = '2021-04-08'
Period = '24'
# x = rq.get('https://api.bmreports.com/BMRS/STORAW/?APIKey=g0t43vms7e1tlk9&FromSettlementDate=2014-12-31&ServiceType=xml/XML')
ws = rq.get('https://api.bmreports.com/BMRS/B1620/V1?APIKey='+ APIKey +'&SettlementDate=' + Date +'&Period='+ Period +'&ServiceType=xml')
#%%
ws = ws.text
wind_root = ET.fromstring(ws)

regen = np.asarray([['fuel', 'power']], dtype = object)

for item in wind_root[1][1]:
    fuel = np.asarray((item[9].text, item[4].text))
    fuel = np.expand_dims(fuel, axis=0)
    regen = np.append(regen, fuel, axis = 0)
    
print(regen)

solarplot = np.asarray(regen[1:])
plt.bar(np.arange(0, np.shape(solarplot)[0]), np.float32(solarplot[:,1]))
plt.xticks(np.arange(0, np.shape(solarplot)[0]), solarplot[:,0], rotation = 'vertical')

#%%