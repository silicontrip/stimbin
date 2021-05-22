#!/usr/local/bin/python3

import math
import pysig as ps
import numpy

lcar = ps.Sine(450,amplitude=ps.DB(-7))
rfm = ps.Add(ps.Sine(3.5,amplitude=50),ps.DC(890))
rcar = ps.Sine(rfm,amplitude=ps.DB(-7))

env = ps.Linear([0,300],[ps.DB(0),ps.DB(0)])

lenv = ps.AM(env,lcar)
renv = ps.AM(env,rcar)

ps.writestereo(lenv,renv,22050,"east-py.wav")

