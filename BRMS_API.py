# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 16:59:19 2021

@author: Matt
"""

import requests as rq
import xml.etree.ElementTree as ET
from lxml import etree
import numpy as np
import matplotlib.pyplot as plt



x = rq.get('https://downloads.elexonportal.co.uk/fuel/download/latest?key=g0t43vms7e1tlk9')
x = x.text


root = ET.fromstring(x)

gen = np.asarray([['fuel', 'power']], dtype = object)

for FUEL in root.findall("./INST/FUEL"):
    fuel = np.asarray((FUEL.attrib["TYPE"], FUEL.attrib["VAL"]))
    fuel = np.expand_dims(fuel, axis=0)
    gen = np.append(gen, fuel, axis = 0)

fuel_plot = np.asarray(gen[1:])
plt.bar(np.arange(0,np.shape(fuel_plot)[0]), fuel_plot[:,1].astype(np.float32))
plt.xticks(np.arange(0,np.shape(fuel_plot)[0]), fuel_plot[:,0], rotation='vertical')
plt.ylabel("Power MW")
plt.tight_layout()
plt.show()

    




