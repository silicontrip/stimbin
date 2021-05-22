#!/bin/sh

for n in $@
do

p=`dirname $0`

o=`echo $n | sed 's/.wav/.am.wav/'`


$p/demod-am.py $n $o


done
