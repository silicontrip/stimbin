#!/bin/sh

for n in $@
do

sing=$( mediainfo $n | grep -c '1 channel')

if [ $sing -eq 1 ]
then
mv $n ../mono
fi

done
