#!/usr/local/bin/python3

import math
from pysig import *

w = 0.075

modrate = \
	Add(
	Add(
	Add( 
	Add(
	Add(
	Add(
	Sine(w,amplitude=0.7), 
	Sine(w*2,amplitude=-0.6)),
	Sine(w*3,amplitude=0.7)),
	Sine(w*4,amplitude=-0.5)),
	Sine(w*5,amplitude=0.4)),
	Sine(w*6,amplitude=-0.18)),
	Sine(w*7,amplitude=0.11))

nmodrate = \
	Add (
		Add(
			Sine(w,amplitude=0.3),
			Sine(w*2,amplitude=-0.0789)
		),
		Sine(w*3,amplitude=0.0551)
	)
mod4rate = \
	Add(
	Add(
	Add(
	Add(
		Sine(w,amplitude=-0.0287),
		Sine(w*2,amplitude=-0.0500)
	),
		Sine(w*3,amplitude=-0.0590)	
	),
		Sine(w*4,amplitude=-0.0548)
	),
		Sine(w*5,amplitude=-0.0407)
	)

mod5rate = \
	Add(
	Add(
	Add(
	Add(
		Sine(w,amplitude=0.1308),
		Sine(w*2,amplitude=-0.0699)
	),
		Sine(w*3,amplitude=0.0617)	
	),
		Sine(w*4,amplitude=-0.004)
	),
		Sine(w*5,amplitude=0.00207)
	)

guess = Sine(191)
for fr in [210,391,410,591,610,791,810,991,1010]:
	guess = Add(Sine(fr),guess)

guess = Div(guess,10)

env = Linear([0,2,298,300],[0,0.5,0.5,0])

out = AM (env,guess)

write(out,sps=11025,name="modgrate.wav")


# L -11..-1 50Hz
# R -4..-1 20Hz

# 85,  1910, 2100, 3910, 4100, 5910, 6100, 7910, 8100, 9910, 10100