#!/usr/local/bin/python3
import pysig as ps
from pysig import DB

# I might use this as a reference
car2 = ps.Square(1000,amplitude=DB(-6)) 

sig=ps.AM(ps.Linear([0,2,9.9,10],[0,1,1,0]), car2)


sil = ps.Linear([0,2],[0,0])

car = ps.Sine(3200)

for fdb in range (-75,1):
	db = fdb / 3
	env=ps.Linear([0,0.1,0.9,1],[0,DB(db),DB(db),0])
	lsig = ps.AM(env,car)
	sig = ps.Cat(sig,lsig)

#ps.plotsig(sig,1024)

ps.write(sig,sps=22050,name="0.sifav.wav")

