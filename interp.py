#!/usr/local/bin/python3

import matplotlib.pyplot as plt
import math
import sys
import numpy

def sinc(x):
	if (x==0): 
		return 1
	return math.sin(math.pi * x) / (math.pi * x) 

def bspline(x):
	if (abs(x)>= 2):
		return 0
	if (abs(x) >= 1):
		return (-1/6) * abs(x) ** 3 + x**2 - 2 * abs(x) + 4 / 3
	return 1/2 * abs(x) **3  - x ** 2 + 2 / 3

def coin(x):
	if (abs(x) > 1):
		return 0
	return (math.cos(x*math.pi) + 1) / 2

def lin(x):
	if (abs(x) > 1):
		return 0
	return 1- abs(x)  

def getratio(ev,inp):
	inp *= ev.__len__()
	ptz = [x-inp for x in range(ev.__len__())]
	win=[]
	wint=0

	win = numpy.array([bspline(p) for p in ptz])
	wint = win.sum()
	
	tt=0
	for pp in range(ev.__len__()):
		vv = win[pp]
		if (wint != 0 and wint != 1):
			vv /= wint
		tt += ev[pp] * vv
	
	return tt


ev=[int(x) for x in sys.argv[1].split(',')]
res=256
outp=[]

outp = [getratio(ev,x/res) for x in range(0,res)]

plt.plot(outp)
plt.show()
