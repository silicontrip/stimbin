#!/usr/local/bin/python3
import pysig as ps

#mod = ps.Linear([0,60,300],[0.25,8,100]) # half

mod = ps.Linear([0,600],[0.25,4])
hmod = ps.Div(mod,2.0)
smod = ps.Add(ps.Sine(0.05,amplitude=hmod),mod)
#mod =ps.Sine(0.01,amplitude=10)

#carrier = ps.Square( ps.Add(ps.DC(900),smod) )
#carriel = ps.Square( ps.Add(ps.DC(900),ps.Negative(smod)) )

carrier = ps.Sine( ps.Add(ps.DC(900),smod) )
carriel = ps.Sine( ps.Add(ps.DC(900),ps.Negative(smod)) )


env = ps.Linear([0,2,30,600],[ps.DB(-96),ps.DB(-7),ps.DB(-5),ps.DB(-3)])
envcar = ps.AM(env,carrier)
envcal = ps.AM(env,carriel)


ps.write(envcal,envcar,sps=22050,name="sipha3.wav")
#ps.writemono(envcar,22050,"sisq-mplex.wav")

