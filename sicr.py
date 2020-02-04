#!/usr/local/bin/python3
import pysig as ps

carrier = ps.Sine(2400)
sig = ps.Div(ps.Add(ps.Add(ps.Sine(60), ps.Sine(120)),0.5),2.5)

sigcar = ps.AM(sig,carrier)

env = ps.Linear([0,2,60,300],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-5)])
envcar = ps.AM(env,sigcar)


ps.write(envcar,sps=22050,name="sicr.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

