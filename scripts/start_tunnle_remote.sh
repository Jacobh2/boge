#!/bin/bash

while true
do
	echo "Check if we can resolve URL"

	hostname_to_resolve="<domain>"
	timeout_seconds=120

	echo "Waiting for hostname to be resolved: $hostname_to_resolve"

	timeout_start=$(date +%s)
	while true; do
		if host "$hostname_to_resolve" >/dev/null 2>&1; then
			echo "Hostname resolved: $hostname_to_resolve"
			break
		fi

		current_time=$(date +%s)
		elapsed_time=$((current_time - timeout_start))

		if [ "$elapsed_time" -ge "$timeout_seconds" ]; then
			echo "Timeout reached. Hostname could not be resolved within $timeout_seconds seconds."
			exit 1
		fi

		sleep 1
	done

	echo "Starting tunnle in 10 sec"
	sleep 10
	echo "Starting tunnle now"
	ssh -v -o ServerAliveInterval=60 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -N -R 9091:0.0.0.0:22 jacobhagstedt@<domain> -p <port>
	echo "Tunnle failed, sleep 1 minute and try again"
	sleep 55
	echo "Starting again in 5 sec"
	sleep 5
done