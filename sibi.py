#!/usr/local/bin/python3
import math
import pysig as ps
from pysig import DB
#import matplotlib.pyplot as pt
#import numpy

env = ps.Linear([0,2,60,300],[DB(-96),DB(-7),DB(-5),DB(-5)])
carrier = ps.Bipolar(600)

envcar = ps.AM(env,carrier)

ps.write(envcar,sps=22050,name="sibi.wav")

