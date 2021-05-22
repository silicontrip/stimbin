#!/bin/sh


if [ ! -z "$1" ]
then

	for n in $@
	do
		l=$(basename $n)
		if [ -e $l ]
		then
			cmp -s $l $n
			if [ $? -eq 1 ]
			then
				echo $n
				rm $l
				ln $n $l
			fi
		else
			echo "NF $l"
		fi
	done
fi

		

