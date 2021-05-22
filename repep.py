#!/usr/local/bin/python3

import math
from pysig import *

def fminator():
	fre = Sine(6,amplitude=400)
	amp = Sine(6,amplitude=2.5)

	lcar = Sine(Add(600,fre))
	rcar = Sine(Add(600,Negative(fre)))

	lmod = AM(lcar,DBS(Add(-5.5,amp)))
	rmod = AM(rcar,DBS(Add(-5.5,Negative(amp))))

	amf = Linear ([0,300],[0.22,0.44])
	am = Add(Square(amf,duty=2/3,amplitude=0.5),0.5)

	rmod2 = AM(am,rmod)

	env = Linear([0,2,30,300],[DB(-96),DB(-7),DB(-5),DB(-3)])

	lenv = AM(env,lmod)
	renv = AM(env,rmod2)

	write(lenv,renv,sps=22050,name="repep-fm.wav")

def wantto():

	car = Sine(6000)
	lmod = Unitise(Square(100))

	rmod = Unitise(Sine(20))

	rmf = Linear([0,300],[0.666,3])
	rrmod = Unitise(Sawtooth(rmf))

	lsig = AM(car,lmod)
	rsig = AM(car,rmod)
	rrsig = AM(rsig,rrmod)

	env = Linear([0,2,30,300],[DB(-96),DB(-7),DB(-5),DB(-3)])
	lenv = AM(env,lsig)
	renv = AM(env,rrsig)

	write(lenv,renv,sps=22050,name="repep-wantto2.wav")

def twine():

	#car = Sine(800)
	pha = Linear([0,600],[0.666,6])

	lcar = Sine(Add(600,pha))
	rcar = Sine(Add(600,Negative(pha)))

	rmod = Scale(Square(80),outscale=[DB(-21),DB(0)])

	lmpx = Square(40)
	lmod1 = Scale(Sine(80,phase=-math.pi/2),outscale=[DB(-24),DB(-18)])
	lmod2 = Scale(Sine(80,phase=-math.pi/2),outscale=[DB(-2),DB(0)])

	lsig1 = AM(lcar,lmod1)
	lsig2 = AM(lcar,lmod2)
	lsig = Mplex(lmpx,lsig1,lsig2)
	rsig = AM(rcar,rmod)

	env = Linear([0,2,598,600],[0,DB(-2),DB(-2),0])
	lenv = AM(env,lsig)
	renv = AM(env,rsig)

	write(lenv,renv,sps=22050,name="repep-te-600.wav")

def cuci():

	car = Sine(800)

	lfre = Linear([0,600],[0.666,6])
	lmods = Scale(Sine(lfre),outscale=[0,1])
	lmodq = Scale(Square(20),outscale=[DB(-18),DB(-3)])

	rmod = Scale(Square(100),outscale=[DB(-12),DB(-3)])

	lsig = AM(AM(car,lmods),lmodq)
	rsig = AM(car,rmod)

	env = Linear([0,2,598,600],[DB(-96),DB(-3),DB(-3),DB(-96)])
	lenv = AM(env,lsig)
	renv = AM(env,rsig)

	write(lenv,renv,sps=22050,name="repep-cu-l.wav")

#fminator()
#wantto()
#twine()
cuci()
