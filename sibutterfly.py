#!/usr/local/bin/python3
import pysig as ps


amod = ps.Scale(ps.AbsSig(ps.Sine(9)),[0,1],[ps.DB(-8),ps.DB(-4)])
#,[-1,1],[ps.DB( # 9hz am -8db - -4db
fmod = ps.Add(ps.Sine(1/8,amplitude=15),765) # 1/8 fm  750-780 hz x1 x3 x5
fmod3 = ps.AM(fmod,3)
fmod5 = ps.AM(fmod,5)

tcar = ps.Add(ps.Sine(fmod),ps.Sine(fmod3))
car = ps.Add(tcar,ps.Sine(fmod5))



mod = ps.AM(amod,car)


#plot=ps.Linear([0,0.01],[1,1])
#ec = ps.AM(plot,car)
#ps.plotsig (ec,5120)

env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])

sig = ps.AM(env,mod)

ps.write(sig,sps=22050,name="sibu.wav")

