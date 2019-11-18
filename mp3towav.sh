#!/bin/sh

for n in $@
do

o=`echo $n | sed 's/.mp3/.wav/'`
ffmpeg -y -i $n $o

done
