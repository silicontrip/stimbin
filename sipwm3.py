#!/usr/local/bin/python3
import math
import pysig as ps
from pysig import DB
import matplotlib.pyplot as pt
import numpy


lamp = ps.Unitise(ps.Wave("NiteRider.am.wav",channel=0))
lcar = ps.Square(440,duty=lamp)

ramp = ps.Unitise(ps.Wave("NiteRider.am.wav",channel=1))
rcar = ps.Square(440,duty=ramp)

ps.write(lcar,right=rcar,sps=44100,name="sipwm3.wav")

