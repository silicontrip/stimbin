# stimbin
python signal generator

## Overview
A highly flexible signal generation library.  Using OO polymorphism to represent signal generators.  These signal classes can be either stand alone, 
like sine, square or random, linear.  Or can take another signal and modify it, such as Hilbert, negative, AM.  Each signal class is inherited from
the same Signal base class, chaining of classes can make complex signal generators.

## Example 
```
mod = ps.Linear([0,300],[0.666,3])
lcar = ps.Sine(ps.Add(570,ps.Negative(mod)))
rcar = ps.Div(ps.Add(ps.Sine(330),ps.Add(ps.Sine(ps.Add(570,mod)),ps.Sine(1470))),3)

bmod = ps.Sine(mod)
rmod = ps.Scale(bmod,outscale=[0,1])
lmod = ps.Scale(ps.Hilbert(bmod),outscale=[0,1])

lsig = ps.AM(lmod ,lcar)
rsig = ps.AM(rmod,rcar)
env = ps.Linear([0,2,300],[0,ps.DB(-3),ps.DB(-3)])
lenv = ps.AM(env, lsig)
renv = ps.AM(env , rsig)
```
- The first line generates a linear ramp from 2/3Hz to 3Hz over the period of 300 seconds and assigns that to 'mod'
- lcar (left carrier) is assigned a Sine wave of 570Hz minus mod
- rcar is 3 sine waves added together, of Frequencies 330Hz, 570Hz plus mod and 1470 Hz then divided by 3 to normalise the signal.
- bmod is a sine wave of mod frequency.
- rmod is a normalised bmod, scaled from -1..+1 to 0..1
- lmod is a Hilbert transform of the bmod signal and normalised (A Hilbert transform shifts a signal by 90 degrees)
- lsig is an Amplitude modulation of lmod with lcar.
- rsig the same.
- an envelope is made with the amplitude 0 (approx -96dB) to -3dB over 2 seconds then hold at -3dB until 300 seconds.
- This envelope is modulated with the left and right signals.

A wave file is then written with ps.write

The output from one signal generator can be used as an input to another signal generator.
Some generators have inputs for more than 1 type of modulation.  Square waves can modulate their duty cycle. Sine waves can not only 
modulate their freqency but phase and amplitude also.
