#!/usr/local/bin/python3

import math
import pysig as ps

def partOne():
	car = ps.Bipolar(400)
	rmf = ps.Linear([0,120],[1,4])
	lmf = ps.Div(rmf,7)
	rmod=ps.Scale(ps.Square(rmf,duty=0.1),outscale=[0,ps.DB(-12)])
	lmod=ps.Scale(ps.Sine(lmf),outscale=[ps.DB(-15),ps.DB(-10)])
	env=ps.Linear([0,2,120],[0,1,1])
	lsig = ps.AM(lmod,car)
	rsig=ps.AM(rmod,car)

	renv=ps.AM(rsig,env)
	lenv=ps.AM(lsig,env)

	ps.write(lenv,renv,sps=22050,name="erem1.wav")

def partTwo():
	car = ps.Bipolar(400)
	bmf = ps.Linear([0,120],[1,4])
	rmf = ps.AM(5,bmf)
	lmf = ps.Div(bmf,4)

	rmod=ps.Scale(ps.Square(rmf,duty=0.1),outscale=[0,ps.DB(-12)])
	lmod=ps.Scale(ps.Sine(lmf),outscale=[0,ps.DB(-6)])
	env=ps.Linear([0,2,120],[0,1,1])
	lsig = ps.AM(lmod,car)
	rsig=ps.AM(rmod,car)

	renv=ps.AM(rsig,env)
	lenv=ps.AM(lsig,env)

	ps.write(lenv,renv,sps=22050,name="erem2.wav")

def partThree():
	# 400Hz - 2000Hz
	# -16dB - -9dB
	# -13db -  -6dB

	bmf = ps.Linear([0,15],[1,1.5])

	mif = ps.Linear([0,15],[ps.DB(-16),ps.DB(-13)])
	maf = ps.Linear([0,15],[ps.DB(-9),ps.DB(-6)])

	mf = ps.Sine(bmf)
	hf = ps.Div(mf,2.0)


	fr = ps.Scale(mf,outscale=[400,2000])
	# feature request, signalise the outscale values... done
	am = ps.Scale(mf,outscale=[mif,maf])

#	ps.write(fr,sps=22050,name="eremfr.wav")
	#ps.plotsig(fr)
	lfr = ps.Sine(ps.Add(fr, bmf))
	rfr = ps.Sine(ps.Add(fr, ps.Negative(bmf)))
	
	#ps.write(lfr,rfr,sps=22050,name="erenv.wav")
	lenv = ps.AM(am,lfr)
	renv = ps.AM(am,rfr)
	ps.write(lenv,renv,sps=22050,name="erem3.wav")

def partFour():
	# right bi-polar 400Hz AM square 0.25Hz 50%  AM sine(0..1) 6Hz -4dB..0dB 
	# left bi-polar sine(0..1) 2Hz  -4dB..0dB

	kmod = ps.Linear([0,120],[ps.DB(-4),ps.DB(0)])
	fmod = ps.Linear([0,120],[0.25,4])

	#bcar = ps.Bipolar(400)

	lcar = ps.Bipolar(ps.Add(400,fmod))
	rcar = ps.Bipolar(ps.Add(400,ps.Negative(fmod)))

	sqmod = ps.Scale(ps.Square(fmod))
	simod = ps.Scale(ps.Sine(ps.AM(ps.DC(4),fmod)))
	lsig = ps.AM(lcar,simod)
	rsig = ps.AM(sqmod, ps.AM(rcar,ps.Sine(6)))

	lenv = ps.AM(lsig,kmod)
	renv = ps.AM(rsig,kmod)

	ps.write(lenv,renv,sps=22050,name='erem4.wav')

def partSix():
	pass
	# left bipolar 400Hz AM -10dB..-5dB @ 65s
	# right bipolar 400Hz AM -10dB..-5dB @ 65s env 0s/0 .. 0.1s/0 .. 0.14s/100 .. 0.2s/100 .. 0.21s/0


def partSeven():
	# 400Hz - 2000Hz
	# -16dB - -9dB
	# -13db -  -6dB

	bmf = ps.Linear([0,55],[1,2.8333])

	mif = ps.Linear([0,30,55],[ps.DB(-16),ps.DB(-11),ps.DB(-11)])
	maf = ps.Linear([0,30,55],[ps.DB(-9),ps.DB(-3),ps.DB(-3)])

	mf = ps.Sine(bmf)
	hf = ps.Div(mf,2.0)


	fr = ps.Scale(mf,outscale=[400,2000])
	# feature request, signalise the outscale values... done
	am = ps.Scale(mf,outscale=[mif,maf])

#	ps.write(fr,sps=22050,name="eremfr.wav")
	#ps.plotsig(fr)
	lfr = ps.Sine(ps.Add(fr, bmf))
	rfr = ps.Sine(ps.Add(fr, ps.Negative(bmf)))
	
	#ps.write(lfr,rfr,sps=22050,name="erenv.wav")
	lenv = ps.AM(am,lfr)
	renv = ps.AM(am,rfr)
	ps.write(lenv,renv,sps=22050,name="erem7.wav")

#partOne()
#partTwo()
#partThree()
#partFour()
#partFive() == partThree()
partSeven()