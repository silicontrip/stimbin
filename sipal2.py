#!/usr/local/bin/python3
import pysig as ps
from pysig import DB

env = ps.Linear([0,1,9,10],[DB(-96),DB(-6),DB(-6),DB(-96)])
fcar = ps.Square(100)
sig = ps.AM(env,fcar)

for hz in range(200,5000,100):
	carrier = ps.Square(hz)
	sigcar = ps.AM(env,carrier)
	sig = ps.Cat(sig,sigcar)	


ps.write(sig,sps=22050,name="sipal100.wav")

