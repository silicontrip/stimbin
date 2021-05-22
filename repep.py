#!/usr/local/bin/python3

import math
<<<<<<< HEAD
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
=======
import pysig as ps

def fminator():
	fre = ps.Sine(6,amplitude=400)
	amp = ps.Sine(6,amplitude=2.5)

	lcar = ps.Sine(ps.Add(600,fre))
	rcar = ps.Sine(ps.Add(600,ps.Negative(fre)))

	lmod = ps.AM(lcar,ps.DBS(ps.Add(-5.5,amp)))
	rmod = ps.AM(rcar,ps.DBS(ps.Add(-5.5,ps.Negative(amp))))

	amf = ps.Linear ([0,300],[0.22,0.44])
	am = ps.Add(ps.Square(amf,duty=2/3,amplitude=0.5),0.5)

	rmod2 = ps.AM(am,rmod)

	env = ps.Linear([0,2,30,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3)])

	lenv = ps.AM(env,lmod)
	renv = ps.AM(env,rmod2)

	ps.write(lenv,renv,sps=22050,name="repep-fm.wav")

def wantto():

	car = ps.Sine(6000)
	lmod = ps.Unitise(ps.Square(100))

	rmod = ps.Unitise(ps.Sine(20))

	rmf = ps.Linear([0,300],[0.666,3])
	rrmod = ps.Unitise(ps.Sawtooth(rmf))

	lsig = ps.AM(car,lmod)
	rsig = ps.AM(car,rmod)
	rrsig = ps.AM(rsig,rrmod)

	env = ps.Linear([0,2,30,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3)])
	lenv = ps.AM(env,lsig)
	renv = ps.AM(env,rrsig)

	ps.write(lenv,renv,sps=22050,name="repep-wantto2.wav")

def twine():

	#car = ps.Sine(800)
	pha = ps.Linear([0,600],[0.666,6])

	lcar = ps.Sine(ps.Add(6000,pha))
	rcar = ps.Sine(ps.Add(6000,ps.Negative(pha)))

	rmod = ps.Scale(ps.Square(80),outscale=[ps.DB(-21),ps.DB(0)])

	lmpx = ps.Square(40)
	lmod1 = ps.Scale(ps.Sine(80,phase=-math.pi/2),outscale=[ps.DB(-24),ps.DB(-18)])
	lmod2 = ps.Scale(ps.Sine(80,phase=-math.pi/2),outscale=[ps.DB(-2),ps.DB(0)])

	lsig1 = ps.AM(lcar,lmod1)
	lsig2 = ps.AM(lcar,lmod2)
	lsig = ps.Mplex(lmpx,lsig1,lsig2)
	rsig = ps.AM(rcar,rmod)

	env = ps.Linear([0,2,30,600],[ps.DB(-96),ps.DB(-7),ps.DB(-3),ps.DB(-3)])
	lenv = ps.AM(env,lsig)
	renv = ps.AM(env,rsig)

	ps.write(lenv,renv,sps=22050,name="repep-te3.wav")

def cuci():

	car = ps.Sine(800)

	lfre = ps.Linear([0,300],[0.666,3])
	lmods = ps.Scale(ps.Sine(lfre),outscale=[0,1])
	lmodq = ps.Scale(ps.Square(20),outscale=[ps.DB(-18),ps.DB(-3)])

	rmod = ps.Scale(ps.Square(100),outscale=[ps.DB(-12),ps.DB(-3)])

	lsig = ps.AM(ps.AM(car,lmods),lmodq)
	rsig = ps.AM(car,rmod)

	env = ps.Linear([0,2,30,300],[ps.DB(-96),ps.DB(-7),ps.DB(-3),ps.DB(-3)])
	lenv = ps.AM(env,lsig)
	renv = ps.AM(env,rsig)

	ps.write(lenv,renv,sps=22050,name="repep-cu.wav")

#fminator()
wantto()
#twine()
#cuci()
>>>>>>> c2ed75a8440e3f98753a7ef7f37ebb0b720606c0
