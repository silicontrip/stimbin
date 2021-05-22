#!/usr/local/bin/python3

import math
from pysig import *

def partOne():
	car = Bipolar(400)
	rmf = Linear([0,120],[1,4])
	lmf = Div(rmf,7)
	rmod=Scale(Square(rmf,duty=0.1),outscale=[0,DB(-12)])
	lmod=Scale(Sine(lmf),outscale=[DB(-15),DB(-10)])
	env=Linear([0,2,120],[0,1,1])
	lsig = AM(lmod,car)
	rsig=AM(rmod,car)

	renv=AM(rsig,env)
	lenv=AM(lsig,env)

	write(lenv,renv,sps=22050,name="erem1.wav")

def partTwo():
	car = Bipolar(400)
	bmf = Linear([0,120],[1,4])
	rmf = AM(5,bmf)
	lmf = Div(bmf,4)

	rmod=Scale(Square(rmf,duty=0.1),outscale=[0,DB(-12)])
	lmod=Scale(Sine(lmf),outscale=[0,DB(-6)])
	env=Linear([0,2,120],[0,1,1])
	lsig = AM(lmod,car)
	rsig=AM(rmod,car)

	renv=AM(rsig,env)
	lenv=AM(lsig,env)

	write(lenv,renv,sps=22050,name="erem2.wav")

def partThree():
	# 400Hz - 2000Hz
	# -16dB - -9dB
	# -13db -  -6dB

	bmf = Linear([0,15],[1,1.5])

	mif = Linear([0,15],[DB(-16),DB(-13)])
	maf = Linear([0,15],[DB(-9),DB(-6)])

	mf = Sine(bmf)
	hf = Div(mf,2.0)

	fr = Scale(mf,outscale=[400,2000])
	# feature request, signalise the outscale values... done
	am = Scale(mf,outscale=[mif,maf])

#	write(fr,sps=22050,name="eremfr.wav")
	#plotsig(fr)
	lfr = Sine(Add(fr, bmf))
	rfr = Sine(Add(fr, Negative(bmf)))
	
	#write(lfr,rfr,sps=22050,name="erenv.wav")
	lenv = AM(am,lfr)
	renv = AM(am,rfr)
	write(lenv,renv,sps=22050,name="erem3.wav")

def partFour():
	# right bi-polar 400Hz AM square 0.25Hz 50%  AM sine(0..1) 6Hz -4dB..0dB 
	# left bi-polar sine(0..1) 2Hz  -4dB..0dB

	kmod = Linear([0,120],[DB(-4),DB(0)])
	fmod = Linear([0,120],[0.25,4])

	#bcar = Bipolar(400)

	lcar = Bipolar(Add(400,fmod))
	rcar = Bipolar(Add(400,Negative(fmod)))

	sqmod = Scale(Square(fmod))
	simod = Scale(Sine(AM(DC(4),fmod)))
	lsig = AM(lcar,simod)
	rsig = AM(sqmod, AM(rcar,Sine(6)))

	lenv = AM(lsig,kmod)
	renv = AM(rsig,kmod)

	write(lenv,renv,sps=22050,name='erem4.wav')

def partSix():
	pass
	# left bipolar 400Hz AM -10dB..-5dB @ 65s
	# right bipolar 400Hz AM -10dB..-5dB @ 65s env 0s/0 .. 0.1s/0 .. 0.14s/100 .. 0.2s/100 .. 0.21s/0


def partSeven():
	# 400Hz - 2000Hz
	# -16dB - -9dB
	# -13db -  -6dB

	bmf = Linear([0,55],[1,2.8333])

	mif = Linear([0,30,55],[DB(-16),DB(-11),DB(-11)])
	maf = Linear([0,30,55],[DB(-9),DB(-3),DB(-3)])

	mf = Sine(bmf)
	hf = Div(mf,2.0)


	fr = Scale(mf,outscale=[400,2000])
	# feature request, signalise the outscale values... done
	am = Scale(mf,outscale=[mif,maf])

#	write(fr,sps=22050,name="eremfr.wav")
	#plotsig(fr)
	lfr = Sine(Add(fr, bmf))
	rfr = Sine(Add(fr, Negative(bmf)))
	
	#write(lfr,rfr,sps=22050,name="erenv.wav")
	lenv = AM(am,lfr)
	renv = AM(am,rfr)
	write(lenv,renv,sps=22050,name="erem7.wav")

def custom():
	# 400Hz - 2000Hz
	# -16dB - -9dB
	# -13db -  -6dB

	bmf = Linear([0,360],[1,5.33333])

	mif = Linear([0,2,360],[DB(-16),DB(-11),DB(-11)])
	maf = Linear([0,2,360],[DB(-9),DB(-3),DB(-3)])

	mf = Sine(bmf)
	hf = Div(mf,2.0)


	fr = Scale(mf,outscale=[400,800])
	# feature request, signalise the outscale values... done
	am = Scale(mf,outscale=[mif,maf])

#	write(fr,sps=22050,name="eremfr.wav")
	#plotsig(fr)
	lfr = Sine(Add(fr, bmf))
	rfr = Sine(Add(fr, Negative(bmf)))
	
	#write(lfr,rfr,sps=22050,name="erenv.wav")
	lenv = AM(am,lfr)
	renv = AM(am,rfr)
	write(lenv,renv,sps=22050,name="milk8.wav")

#partOne()
#partTwo()
#partThree()
#partFour()
#partFive() == partThree()
#partSeven()

custom()
