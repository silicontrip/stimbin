#!/usr/local/bin/python3
import math
import pysig as ps
#import matplotlib.pyplot as pt
#import numpy


freq= ps.Linear([0,300],[100,5000])
osc = ps.Square(freq)

env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
ienvcar = ps.AM(env,osc)


ps.write(ienvcar,sps=22050,name="sisq-5000.wav")

