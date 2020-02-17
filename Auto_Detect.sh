#!/bin/bash

emma_check=$(ps -ef | grep -v "grep" | grep "python3 -u main.py" | awk '{print $2}')
#echo $emma_check
date=$(date "+%Y-%m-%d_%H:%M:%S")

if [ $emma_check ]; then
	printf "%s : python run %s\t" $date $emma_check
	#echo "inPut command : $1"
	if [ "$1" == 'restart' ]; then
		echo "restart"
		kill $emma_check
		python3 -u main.py &
	else
		echo "Command Not Found..."
	fi
else
	echo "$date : python not run"
	python3 -u main.py &
fi
