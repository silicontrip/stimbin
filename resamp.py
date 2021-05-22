#!/usr/local/bin/python3

import math

import sys
import scipy.signal
import scipy.io.wavfile
import numpy
import argparse

windowresolution=65536

def genlanczos(a):
	
	win=numpy.ones(windowresolution*25+1)
	for x in range(1,windowresolution*25+1):
		nx= x / windowresolution
		win[x] = numpy.sinc(nx) * numpy.sinc(nx*a) 

	return win

def lanczos (xx):
	global lanczoswindow
	#if (xx > lanczoswindow):
	#	return 0
	return lanczoswindow[xx]

def norm (pp):
	tt = pp.sum()

	if (tt == 1 or tt==0):
		return pp
	
	pp = pp / tt

	return pp

def pointlanczos(sp,ratio):
	# generate points for the convolution
	global windowresolution
	ressp = windowresolution * sp
	#print("resp-> ",ressp)
	isp = int(ressp) % windowresolution
	rwin = int (ratio*windowresolution)
	st =  isp - rwin * 3
	ed = isp + rwin * 3
	#print (st,ed,rwin)
	vv = numpy.arange(st,ed,rwin)
	#print(vv)
	avv= numpy.abs(vv)
	#print(avv)
	return avv

def makelanczos(sp,ratio):
	points = pointlanczos(sp,ratio)
	#print(points)
	coef = lanczos(points)
	#print (points,coef)
	return norm(coef)

def interpolatelanczos(sp,ratio,sig):
	ss= sig.__len__()
	st = math.ceil(sp - ratio) 
	ed = math.floor(sp + ratio) +1
	lancwindow = makelanczos(sp,ratio)

	if (st<0):
		st=0
	if (ed>=ss):
		ed=ss-1
	rs = numpy.convolve(lancwindow,sig[st:ed],mode='valid')

	#print(rs)

	return rs[0]
	
parser = argparse.ArgumentParser(description='samplerate modulate a wave signal.')
parser.add_argument("files", nargs='+', help='wave files')
parser.add_argument("-C", "--channel", dest="channel", action='store', help="decode only channel C")

args = parser.parse_args()

print("Generating lanczos")
lanczoswindow = genlanczos(3)
print("Done.")

for fn in args.files:
	sps,aud = scipy.io.wavfile.read(fn)
	
	samples=aud.shape
	
	chan = 1
	if (len(samples)>1):
		(samples,chan) = samples
	else:
			samples,=samples

	print("SPS: " + str(sps))
	print("Channels: " + str(chan))
	print("Samples: " + str(samples))
	

	caud = aud.transpose()
	
	if chan == 1:
		caud = numpy.array([caud])
	
	if (args.channel):
		selchan = int(args.channel)
		#print caud[selchan]
		caud=numpy.array([caud[selchan]])
	
	# print caud
	
	naud=[]

	for a in caud:
		#print(a)
		osp=0
		ncha =[]
		oop=0
		for isp in range(0,samples):
			rat = (osp / samples) * 7 + 1 # ratio function. could be from a wave file.

			if (osp < samples):
				nsamp = interpolatelanczos(osp,rat,a) 
				#nsamp=a[math.floor(osp)]
				irsamp = int(round(nsamp))
				#print(irsamp)
				ncha.append(irsamp)
			else:
				break

			osp += rat # would rather an absolute function

			if (oop != math.floor(osp/samples*100)):
				print(rat,isp,osp/samples*100,nsamp)	
				oop =math.floor(osp/samples*100)


		naud.append(ncha)
	
	npaud = numpy.array(naud) 
	nfn = fn.replace(".wav",".rlin1-8.wav")
	wavout=numpy.array(npaud.transpose(),dtype='int16')
	scipy.io.wavfile.write(nfn,sps,wavout)
