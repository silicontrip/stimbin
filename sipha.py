#!/usr/local/bin/python3
import pysig as ps

#mod = ps.Linear([0,60,300],[0.25,8,100]) # half

mod = ps.Linear([0,30,30.1,126,126.1,174,174.1,198,198.1,210,210.1,216,216.1,219,219.1,221,221.1,223.5,223.6,263,263.1,311],[0.01,0.01,0.1,2,1,3,1.5,3.5,1.75,7.5,3.75,7.7,3.8,7.8,3.9,7.9,4,8,16,16,8,0.1]) # half
mod = ps.Linear([0,600],[0.25,8])
smod = ps.Sine(mod)
#mod =ps.Sine(0.01,amplitude=10)

carrier = ps.Square( ps.Add(ps.DC(100),smod) )
carriel = ps.Square( ps.Add(ps.DC(100),ps.Negative(smod)) )



env = ps.Linear([0,2,30,600],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3)])
envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=22050,name="sipha1.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

