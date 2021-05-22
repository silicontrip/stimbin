#!/bin/sh

for n in $@
do
	lame --preset extreme $n
done
