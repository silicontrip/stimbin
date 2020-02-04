#!/usr/local/bin/python3
import math
import pysig as ps
from pysig import DB
#import matplotlib.pyplot as pt
#import numpy

env = ps.Linear([0,2,60,300],[DB(-96),DB(-7),DB(-5),DB(-5)])

ramp = ps.Linear([0,30,60,90,120,150,180,210,240,270,300],[0,1,0,1,0,1,0,1,0,1,0])  # i don't know why this value needs to be halved.
amp = ps.Square(440,duty=ramp)

envcar = ps.AM(env,amp)

ps.write(envcar,sps=22050,name="sipwm.wav")

