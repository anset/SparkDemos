#!/bin/bash

# Get the amount of lines in the text file
max=`cat ${1} | wc -l`

while :
do
	# Echo a random line from the text file
	line=$(( ( RANDOM % ${max} )  + 1 ))
	sed "${line}q;d" ${1}
done

