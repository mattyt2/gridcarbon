# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 19:54:45 2021

@author: Matt
"""

import requests as rq
import xml.etree.ElementTree as ET
import numpy as np

APIKey = 'g0t43vms7e1tlk9'
Date = '2021-04-02'
Period = '1'
# x = rq.get('https://api.bmreports.com/BMRS/STORAW/?APIKey=g0t43vms7e1tlk9&FromSettlementDate=2014-12-31&ServiceType=xml/XML')
ws = rq.get('https://api.bmreports.com/BMRS/B1630/V1?APIKey='+ APIKey +'&SettlementDate=' + Date +'&Period='+ Period +'&ServiceType=xml')
#%%
ws = ws.text
wind_root = ET.fromstring(ws)

regen = np.asarray([['fuel', 'power']], dtype = object)

for item in wind_root[1][1]:
    fuel = np.asarray((item[2].text, item[5].text))
    fuel = np.expand_dims(fuel, axis=0)
    regen = np.append(regen, fuel, axis = 0)
    
print(regen)
#%%