import math
import numpy
import scipy.io.wavfile
import scipy.signal
import scipy.integrate

import matplotlib.pyplot as pt

def DB(db):
	return 10 ** (db / 20.0)	

def write(signalleft,right=None,sps=44100,name="out.wav"):
	dur = signalleft.duration()
	print("Duration:" + str(dur) + " sps: " + str(sps) )
	sample=numpy.arange(0,dur,1/sps)
	sleft = signalleft.getsample(sample)
	if right is not None:
		sright = right.getsample(sample)
		out = numpy.array([sleft*32767,sright * 32767]).astype(numpy.int16)
		scipy.io.wavfile.write(name, sps, numpy.transpose(out))
	else:
		sleft *= 32767
		scipy.io.wavfile.write(name, sps, sleft.astype(numpy.int16))

def writestereo(sigl,sigr,sps,name):
	dur = sigl.duration()
	sample=numpy.arange(0,dur,1/sps)
	left = sigl.getsample(sample)
	right = sigr.getsample(sample)
	out = numpy.array([left,right])

	scipy.io.wavfile.write(name, sps, numpy.transpose(out))

def writemono(sigl,sps,name):
	dur = sigl.duration()
	sample=numpy.arange(0,dur,1/sps)
	left = sigl.getsample(sample)

	scipy.io.wavfile.write(name, sps, left)

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
		dur = self.duration()
		sample=numpy.arange(0,dur,1/sps)
		wavout = self.getsample(sample)

		scipy.io.wavfile.write(name, sps, wavout)

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

class AbsSig(SignalGenerator):

	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.abs(self.signal.getsample(time))

	def duration(self):
		return self.signal.duration()

class Negative(SignalGenerator):

	signal=SignalGenerator()

	def __init__(self,sig):
		self.signal = signal(sig)

	def getsample(self,time):
		return numpy.negative(self.signal.getsample(time))

	def duration(self):
		return self.signal.duration()

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

class Bipolar(Sine):
	amplitude = 0
	hertz = 0
	phase = 0
	dur=0
	pduty=0.5
	nduty=0.5
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

	def getsample(self,time):
		hza = self.hertz.getsample(time)
		pha = self.phase.getsample(time)

		timea = scipy.integrate.cumtrapz(hza,time,initial=0)


		timea = timea * 2 * math.pi
		timea = timea + pha
		# need to do pwm
		return self.amplitude.getsample(timea) * numpy.interp(timea,[-math.pi,math.pi],[-1,1],period=2*math.pi)

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

class Wave(SignalGenerator):
	samples = 0
	sps = 1
	audio = numpy.ndarray([])
	periodic=False

	def __init__(self,name,channel=0,periodic=False,duration=None):
		self.sps,aud = scipy.io.wavfile.read(name)

		self.samples=aud.shape
		self.periodic=periodic

		chan = 1
		if (len(self.samples)>1):
			(self.samples,chan) = self.samples

		# override sample rate to get desired duration.
		if duration is not None:
			self.sps = duration * samples

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
		return numpy.where (spos<=self.samples,self.audio[spos],0)
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
