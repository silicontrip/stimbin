#!/usr/local/bin/python3
import pysig as ps
import matplotlib.pyplot as pt
import numpy


#mod = ps.Linear([0,60,300],[0.25,8,100]) # half

head = ps.Linear([0,30,30.1],[0.01,0.01,0.1])
tail = ps.Linear([0,0.1,40,40.1,88],[4,16,16,4,0.1])

ev = ps.Linear([0,0.5,192.9,193.4],[0,1,1,0])

spc = ps.Sine(0.1,amplitude=0.25)
spe = ps.AM(ev,spc)


ramp = ps.Linear([0,193.4],[0.1,4])

cs = ps.Add(ramp,spe)



hcs = ps.Cat(head,cs)
mod = ps.Cat(hcs,tail)
#pt.plot(mod.getsample(numpy.arange(0,311,0.01)))
#pt.show()

car  = ps.Sine(600)


carrier = ps.Sine( ps.Add(600,mod) )
carriel = ps.Sine( ps.Add(600,ps.Negative(mod)) )



env = ps.Linear([0,2,30,223,263,307,311],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3),ps.DB(-3),ps.DB(-7),ps.DB(-96)])
envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=22050,name="siss1.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

