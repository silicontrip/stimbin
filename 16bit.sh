#!/bin/sh

for n in $@
do
	sf=$(ffmpeg -i $n 2>&1  |grep pcm_f64le -c)
	if [ $sf -eq 1 ]
	then
		ffmpeg -i $n -acodec pcm_s16le ${n}.16.wav
	fi
done
