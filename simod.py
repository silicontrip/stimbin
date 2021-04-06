#!/usr/local/bin/python3
import pysig as ps

mod = ps.Linear([0,60,300],[0.25,8,100]) # half


carrier = ps.Sine( ps.Add(ps.DC(700),mod) )
carriel = ps.Sine( ps.Add(ps.DC(700),ps.Negative(mod)) )



env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=22050,name="simod.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

