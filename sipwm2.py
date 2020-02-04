#!/usr/local/bin/python3
import math
import pysig as ps
from pysig import DB
#import matplotlib.pyplot as pt
#import numpy

env = ps.Linear([0,2,60,300],[DB(-96),DB(-7),DB(-5),DB(-5)])

ramp = ps.Linear([0,300],[0,4])
sramp = ps.Sine(ramp)
pramp = ps.Add(sramp,1)
spramp = ps.Div(pramp,2)
car = ps.Square(440,duty=spramp)
#stimamp = ps.AM(spramp,car)
envcar = ps.AM(env,car)

ps.write(envcar,sps=22050,name="sipwm2.wav")

