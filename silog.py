#!/usr/local/bin/python3
import pysig as ps
from pysig import DB
#import matplotlib.pyplot as pt
#import numpy

env = ps.Log(ps.Linear([0,2],[1,100]))

ps.plotsig(env)
