#!/usr/local/bin/python3
import pysig as ps
from pysig import DB

env = ps.Linear([0,1,9,10],[DB(-96),DB(-6),DB(-6),DB(-96)])
fcar = ps.Sine(100)
sig = ps.AM(env,fcar)

for hz in range(101,111):
	carrier = ps.Sine(hz)
	sigcar = ps.AM(env,carrier)
	sig = ps.Cat(sig,sigcar)	

sig = ps.Cat(sig,ps.DC(0,duration=1))
for hz in range(120,210,10):
	carrier = ps.Sine(hz)
	sigcar = ps.AM(env,carrier)
	sig = ps.Cat(sig,sigcar)	

sig = ps.Cat(sig,ps.DC(0,duration=1))
for hz in range(300,1100,100):
	carrier = ps.Sine(hz)
	sigcar = ps.AM(env,carrier)
	sig = ps.Cat(sig,sigcar)	

sig = ps.Cat(sig,ps.DC(0,duration=1))
for hz in range(2000,11000,1000):
	carrier = ps.Sine(hz)
	sigcar = ps.AM(env,carrier)
	sig = ps.Cat(sig,sigcar)	

ps.write(sig,sps=22050,name="sigHZpallete.wav")

