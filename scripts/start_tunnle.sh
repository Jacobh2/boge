#!/bin/bash

while true
do
	echo "Connecting..."
	ssh -v -N -L 8123:localhost:8123 jacobhagstedt@localhost -p 9091
	echo "Lost ssh connection, waiting 5 sec and will try again"
	sleep 5
	echo "Testing second time..."
	ssh -v -N -L 8123:localhost:8123 jacobhagstedt@localhost -p 9091
	echo "Lost ssh connection, waiting 1 minute and try again"
	sleep 55
	echo "Restarting in 5"
	sleep 5
done
