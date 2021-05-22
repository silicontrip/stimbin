import math
import numpy
import numpy.random
import scipy.io.wavfile
import scipy.signal
import scipy.integrate

import matplotlib.pyplot as pt

def DB(db):
	return 10 ** (db / 20.0)

def Degrees(deg):
	return deg / 180 * math.pi

def write(signalleft,right=None,sps=44100,name="out.wav"):
	dur = signalleft.duration()
	if (math.isinf(dur)):
		raise Exception("No Duration defined")
	
	print("Duration:" + str(dur) + " sps: " + str(sps) )
#	sample=numpy.arange(0,dur,1/sps)
	sample=numpy.linspace(0,dur,num=int(sps * dur))
	sleft = signalleft.getsample(sample)
	if right is not None:
		sright = right.getsample(sample)
		out = numpy.array([sleft*32767,sright * 32767]).astype(numpy.int16)
		scipy.io.wavfile.write(name, sps, numpy.transpose(out))
	else:
		sleft *= 32767
		scipy.io.wavfile.write(name, sps, sleft.astype(numpy.int16))

def writestereo(sigl,sigr,sps,name):
	left = sigl.getnd(sps)
	right = sigr.getnd(sps)
	out = numpy.array([left,right])

	scipy.io.wavfile.write(name, sps, numpy.transpose(out))

def writemono(sigl,sps,name):
	scipy.io.wavfile.write(name, sps, sigl.getnd(sps))

def plotsig(sigl,samples=1000,dur=None):
	if (dur is None):
		dur = sigl.duration()
	spl = numpy.arange(0,dur,dur/samples)

	pt.plot(spl,sigl.getsample(spl))	
	pt.show()


def signal(sig):
	if isinstance(sig,SignalGenerator):
		return sig
	if isinstance(sig,float):
		return DC(sig)
	else:
		return DC(float(sig))

class SignalGenerator:

	def duration(self):
		return [0,math.inf]

	def getsample(self, time):
		return numpy.array([])

	def getnd(self,sps):
		dur = self.duration()
		sample=numpy.arange(0,dur,1/sps)
		return self.getsample(sample)

	def write(self,sps,name):
		wavout = self.getnd(sps)
		scipy.io.wavfile.write(name, sps, wavout)

	def getrange(self,index=None):
		if (index is None):
			return [-math.inf,math.inf]
		else:
			return [-math.inf,math.inf][index]

# converts -1 to 1 to 0 to 1. IE standard sine output
class Unitise(SignalGenerator):

	signal=SignalGenerator()

	def __init__(self,sig):
		# probably not needed... why would you unitise a DC signa?
		self.signal = signal(sig)

	def getsample(self,time):
		return ( self.signal.getsample(time) + 1 ) / 2

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return [0,1]
		else:
			return [0,1][index]

class Scale(SignalGenerator):

	signal=SignalGenerator()
#	offset=-0.5
	scale=0.5
	newmin=0
	oldmin=-1
	range =[]

	def __init__(self,sig,inscale=[-1,1],outscale=[0,1]):
		# probably not needed... why would you unitise a DC signa?
		self.signal = signal(sig)
		self.newmin = signal(outscale[0])
		self.oldmin = signal(inscale[0])

		in0 = signal(inscale[0])
	#	plotsig(in0,dur=10)
		in1 = signal(inscale[1])
		#plotsig(in1,dur=10)

		out0 = signal(outscale[0])
		#plotsig(out0,dur=10)

		out1 = signal(outscale[1])
		#plotsig(out1,dur=10)

		intime = Add(in1, Negative(in0))
		#plotsig(intime,dur=10)

		outtime = Add(out1, Negative(out0))
		#plotsig(outtime,dur=10)

		self.scale = Div(outtime,intime)
		#plotsig(self.scale,dur=10)

	#	diff = Add(out0,Negative(in0))
		#plotsig(diff,dur=10)

	#	self.offset = AM(diff , self.scale)
	#	plotsig(self.offset,dur=10)

		#self.scale = (numpy.subtract(signal(outscale[1]), signal(outscale[0])) / (signal(inscale[1])-signal(inscale[0])))
		#self.offset = signal(outscale[0]) - (signal(inscale[0]) * self.scale)

		self.range = [min(out1.getrange(0),out0.getrange(0)), max(out1.getrange(1),out0.getrange(1))]
		#print(self.range)

	def getsample(self,time):
		return ( ( self.signal.getsample(time) - self.oldmin.getsample(time)) * self.scale.getsample(time) ) + self.newmin.getsample(time)

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return self.range
		else:
			return self.range[index]

class AbsSig(SignalGenerator):

	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.abs(self.signal.getsample(time))

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return [0,self.signal.getrange(index=1)]
		else:
			return [0,self.signal.getrange(index=1)][index]

class Negative(SignalGenerator):

	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.negative(self.signal.getsample(time))

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return [0.0-self.signal.getrange(index=0),0.0-self.signal.getrange(index=1)]
		else:
			return 0.0-self.signal.getrange(index=index)

class DC(SignalGenerator):
	y=0
	dur=math.inf

	def __init__(self,amp,duration=None):
		if duration is not None:
			self.dur=duration
		self.y=amp

	def getsample(self,time):
		return numpy.full(time.shape,self.y)

	def duration(self):
		return self.dur

	def getrange(self,index=None):
		if (index is None):
			return [self.y,self.y]
		else:
			return self.y

class Log(SignalGenerator):

	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.log10(self.signal.getsample(time))

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return [0,numpy.log10(self.signal.getrange(index=1))]
		else:
			return [0,self.signal.getrange(index=1)][index]

class Linear(SignalGenerator):

	envelope_time = [0,1]
	envelope_amplitude = [0,0]

	def __init__(self, env_time,env_amp):
		self.envelope_time = env_time
		self.envelope_amplitude = env_amp

	def getsample(self,time):
		return numpy.interp(time,self.envelope_time,self.envelope_amplitude)

	def duration(self):
		return max(self.envelope_time)

	def getrange(self,index=None):
		if (index is None):
			return [min(self.envelope_amplitude),max(self.envelope_amplitude)]
		else:
			return [min(self.envelope_amplitude),max(self.envelope_amplitude)][index]



class Sine(SignalGenerator):
	amplitude = 1
	hertz = 0
	phase = 0
	dur = math.inf
	dist = 0
	distpha=0

	def __init__(self,h,amplitude=None,phase=None,duration=None,distortion=None,distortionphase=None):
		if amplitude is None:
			self.amplitude = DC(1)  # 1 = DB(0)
		else:
			self.amplitude = signal(amplitude)
		self.hertz = signal(h)

		if phase is None:
			self.phase = DC(0)
		else:
			self.phase = signal(phase)

		if duration is None:
			self.dur = math.inf
		else:
			self.dur = duration

		if distortion is None:
			self.dist = DC(0)
		else:
			self.dist = signal(distortion)

		if distortionphase is None:
			self.distpha = DC(0)
		else:
			self.distpha = signal(distortionphase)

	def getsample(self,time):
		
		hza = self.hertz.getsample(time)
		pha = self.phase.getsample(time)
		disa = self.dist.getsample(time)
		dpha = self.distpha.getsample(time)

		#pt.plot(time)
		timea = scipy.integrate.cumtrapz(hza,time,initial=0)

		timea = timea * 2 * math.pi
		timeb = timea + dpha
		#timea = timea * hza
		timea = timea + pha

		return self.amplitude.getsample(time) * numpy.sin(timea + disa * numpy.sin(timeb))

	def duration(self):
		return min([self.hertz.duration(), self.phase.duration(), self.amplitude.duration(), self.dur])

	def getrange(self,index=None):
		# arg amplitude
		if (index is None):
			return self.amplitude.getrange()
		else:
			return self.amplitude.getrange(index=index)

class Random(Sine):
	amplitude=1
	hertz=0
	phase=0

	rng=None
	
	def __init__(self,seed,amplitude=None,duration=None):
		self.rng = numpy.random.RandomState(seed)
		self.hertz=DC(0)
		self.phase=DC(0)
		# print(self.rng)

		if amplitude is None:
			self.amplitude = DC(1)  # 1 = DB(0)
		else:
			self.amplitude = signal(amplitude)

		if duration is None:
			self.dur = math.inf
		else:
			self.dur = duration

	def getsample(self,time):
		#print(time.shape)
		return self.amplitude.getsample(time) * self.rng.random_sample(size=time.shape)


class Bipolar(Sine):
	amplitude = 0
	hertz = 0
	phase = 0
	dur=0
	pduty=DC(0.5)
	nduty=DC(0.5)
	duty=0.5

	def __init__(self,h,amplitude=None,phase=None,duty=None,duration=None):
		if amplitude is None:
			self.amplitude = DC(DB(0))
		else:
			self.amplitude = signal(amplitude)

		self.hertz = signal(h)

		if phase is None:
			self.phase = DC(0)
		else:
			self.phase = signal(phase)

		if duty is None:
			self.pduty = DC(0.5)
			self.nduty = DC(0.5)
			self.duty = DC(0.5)
		else:
			self.duty = signal(duty)

		if duration is None:
			self.dur = math.inf
		else:
			self.dur = duration

	def getsample(self,time):
		hza = self.hertz.getsample(time)
		pha = self.phase.getsample(time)
		ama = self.amplitude.getsample(time)

		timea = scipy.integrate.cumtrapz(hza,time,initial=0)

		timea = timea * 2 * math.pi
		timea = timea + pha

		dta = self.duty.getsample(timea)
		dtb = self.pduty.getsample(timea)

		dtc = self.nduty.getsample(timea) # arg minus the other side of the main duty cycle duration. 
		# dta * 1 / hza
		
		mdc = scipy.signal.square(timea,dta)
		#numpy.piecewise(mdc,[x<0,x>=0],[lambda: 
		
		#brain hurts
		
		#,])

		#numpy.piecewise([x<0,x>=0],[1,0])		
		#numpy.piecewise([x<0,x>=0],[0,-1])		

		# scipy.signal.square()

		return ama * numpy.round(numpy.sin(timea))


class Sawtooth(Sine):
	amplitude = 0
	hertz = 0
	phase = 0
	dur = 0
	duty = 0

	def __init__(self,h,amplitude=None,phase=None,duration=None,duty=None):
		if amplitude is None:
			self.amplitude = DC(1)  # 1 = DB(0)
		else:
			self.amplitude = signal(amplitude)
		self.hertz = signal(h)

		if phase is None:
			self.phase = DC(0)
		else:
			self.phase = signal(phase)

		if duration is None:
			self.dur = math.inf
		else:
			self.dur = duration

		if duty is None:
			self.duty = 0.1
		else:
			self.duty = duty * numpy.pi / 50
			# self.duty = signal(duty * numpy.pi / 100 )

	def getsample(self,time):
		hza = self.hertz.getsample(time)
		pha = self.phase.getsample(time)
		dut = self.duty

		timea = scipy.integrate.cumtrapz(hza,time,initial=0)

		timea = timea * 2 * math.pi
		timea = timea + pha
		# need to do pwm
		return self.amplitude.getsample(timea) * numpy.interp(timea,[0,dut,2*numpy.pi],[1,-1,1],period=2*numpy.pi)

		#return self.amplitude.getsample(timea) * numpy.interp(timea,[0,2*numpy.pi],[1,-1],period=2*numpy.pi)

class Square(Sine):
	amplitude = 0
	hertz = 0
	phase = 0
	dur=0
	duty=0.5

	def __init__(self,h,amplitude=None,phase=None,duty=None,duration=None):
		dur = math.inf
		if amplitude is None:
			self.amplitude = DC(DB(0))
		else:
			self.amplitude = signal(amplitude)

		dur = min(self.amplitude.duration(),dur)

		self.hertz = signal(h)

		dur = min(self.hertz.duration(),dur)


		if phase is None:
			self.phase = DC(0)
		else:
			self.phase = signal(phase)

		dur = min(self.phase.duration(),dur)

		if duty is None:
			self.duty = DC(0.5)
		else:
			self.duty = signal(duty)

		dur = min(self.duty.duration(),dur)

		if duration is None:
			self.dur = dur
		else:
			self.dur = duration

	def getsample(self,time):
		hza = self.hertz.getsample(time)
		pha = self.phase.getsample(time)
		ama = self.amplitude.getsample(time)

		timea = scipy.integrate.cumtrapz(hza,time,initial=0)

		timea = timea * 2 * math.pi
		timea = timea + pha

		dta = self.duty.getsample(time)

		#print(hza)
		#print(dta)
		#print()

		return ama * scipy.signal.square(timea,dta)

# same as Multiply
class AM(SignalGenerator):
	sig1 = {}
	sig2 = {}

	def __init__(self,a,b):
		self.sig1 = signal(a)
		self.sig2 = signal(b)

	def getsample (self,time):
		return self.sig1.getsample(time) * self.sig2.getsample(time)

	def duration(self):
		dur1 = self.sig1.duration()
		dur2 = self.sig2.duration()
		return min([dur1,dur2])

	def getrange(self,index=None):
		if (index is None):
			return [self.sig1.getrange(index=0)*self.sig2.getrange(index=0),self.sig1.getrange(index=1)*self.sig2.getrange(index=1)]
		else:
			return [self.sig1.getrange(index=0)*self.sig2.getrange(index=0),self.sig1.getrange(index=1)*self.sig2.getrange(index=1)][index]

class DBS(SignalGenerator):
	sig={}

	def __init__(self,a):
		self.sig=signal(a)

	def getsample(self,time):
		return 10 ** (self.sig.getsample(time) / 20.0)

	def duration(self):
		return self.sig.duration()

class Div(SignalGenerator):
	sig1 = {}
	sig2 = {}

	def __init__(self,a,b):
		self.sig1 = signal(a)
		self.sig2 = signal(b)

	def getsample (self,time):
		return self.sig1.getsample(time) / self.sig2.getsample(time)

	def duration(self):
		dur1 = self.sig1.duration()
		dur2 = self.sig2.duration()
		return min([dur1,dur2])

def getrange(self,index=None):
		if (index is None):
			return [self.sig1.getrange(index=0)/self.sig2.getrange(index=0),self.sig1.getrange(index=1)/self.sig2.getrange(index=1)]
		else:
			return [self.sig1.getrange(index=0)/self.sig2.getrange(index=0),self.sig1.getrange(index=1)/self.sig2.getrange(index=1)][index]

class Hilbert(SignalGenerator):
	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.imag(scipy.signal.hilbert(self.signal.getsample(time)))

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return [0,numpy.imag(scipy.signal.hilbert(self.signal.getrange(index=1)))]
		else:
			return [0,self.signal.getrange(index=1)][index]	

class Gradient(SignalGenerator):
	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.gradient(self.signal.getsample(time))

	def duration(self):
		return self.signal.duration()

	def getrange(self,index=None):
		if (index is None):
			return [0,numpy.gradient(self.signal.getrange(index=1))]
		else:
			return [0,self.signal.getrange(index=1)][index]	


class Add(SignalGenerator):
	sig1 = {}
	sig2 = {}

	def __init__(self,a,b):
		self.sig1 = signal(a)
		self.sig2 = signal(b)

	def getsample (self,time):
		return self.sig1.getsample(time) + self.sig2.getsample(time)

	def duration(self):
		dur1 = self.sig1.duration()
		dur2 = self.sig2.duration()
		return min([dur1,dur2])

	def getrange(self,index=None):
		if (index is None):
			return [self.sig1.getrange(index=0)+self.sig2.getrange(index=0),self.sig1.getrange(index=1)+self.sig2.getrange(index=1)]
		else:
			return [self.sig1.getrange(index=0)+self.sig2.getrange(index=0),self.sig1.getrange(index=1)+self.sig2.getrange(index=1)][index]

class Cat(SignalGenerator):
	sig1 = {}
	sig2 = {}

	def __init__(self,a,b):
		self.sig1 = signal(a)
		self.sig2 = signal(b)

	def getsample (self,time):
		dur1 = self.sig1.duration()
		return numpy.where(time<dur1,self.sig1.getsample(time),self.sig2.getsample(time-dur1))	

	def duration(self):
		dur1 = self.sig1.duration()
		dur2 = self.sig2.duration()
		return dur1+dur2

	def getrange(self,index=None):
		if (index is None):
			return [min(self.sig1.getrange(index=0),self.sig2.getrange(index=0)),max(self.sig1.getrange(index=1),self.sig2.getrange(index=1))]
		else:
			return [min(self.sig1.getrange(index=0),self.sig2.getrange(index=0)),max(self.sig1.getrange(index=1),self.sig2.getrange(index=1))][index]

class Mplex(SignalGenerator):
	sigm={}
	sig1={}
	sig2={}

	def __init__(self,m,a,b):
		self.sigm = signal(m)
		self.sig1 = signal(a)
		self.sig2 = signal(b)

	def getsample (self,time):
		# most signals range from -1 to 1, we need 0 to 1
		inter = (self.sigm.getsample(time) + 1) / 2
		return inter * self.sig1.getsample(time) + (1 - inter) * self.sig2.getsample(time)			

	def duration(self):
		return self.sigm.duration()	

	def getrange(self,index=None):
		if (index is None):
			return [min(self.sig1.getrange(index=0),self.sig2.getrange(index=0)),max(self.sig1.getrange(index=1),self.sig2.getrange(index=1))]
		else:
			return [min(self.sig1.getrange(index=0),self.sig2.getrange(index=0)),max(self.sig1.getrange(index=1),self.sig2.getrange(index=1))][index]

class Wave(SignalGenerator):
	samples = 0
	sps = 1
	audio = numpy.ndarray([])
	periodic=False

	def __init__(self,name,channel=0,periodic=False,duration=None):
		self.sps,aud = scipy.io.wavfile.read(name)

		self.samples=aud.shape
		#print(self.samples)
		self.periodic=periodic

		chan = 1
		
		(self.samples,) = self.samples

		# override sample rate to get desired duration.
		if duration is not None:
			#print("Setting sps = ", self.samples / duration) 
			self.sps =  self.samples / duration

		caud = aud.transpose()

		if chan == 1:
			self.audio = numpy.array(caud) / 32767.0
		else:
			self.audio=numpy.array(caud[channel]) / 32767.0

		#print (self.audio)

	def duration(self):
		return 1.0 * self.samples / self.sps

	def getsample (self,time):
			
		spos = numpy.round(self.sps * time).astype(int)

		if (self.periodic):
			spos = spos % self.samples

		#print(spos.shape)
		#print(self.audio.size)
		#print(self.audio.shape)

		#return self.audio[spos]
		#print( "spos " , spos)
		return self.audio[numpy.where ((spos>=0) & (spos<self.samples), spos,0)]
		#return numpy.piecewise(spos,[spos<=self.samples],[lambda spos: self.audio[spos],0])

#class Dur(SignalGenerator):
#	sig={}
#	dur=[]

#	def __init__(self,m,d):
#		self.sig = signal(m)
#		self.dur = d

#	def getsample (self,time):
#		return self.sig.getsample(time)			

#	def duration(self):
#		return self.dur
