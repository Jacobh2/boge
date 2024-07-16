#!/bin/bash

# Define the SSH command
SSH_CMD="ssh -v -o ServerAliveInterval=60 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -N -R 9091:0.0.0.0:22 jacobhagstedt@icehack.asuscomm.com -p 54324"

# Function to run the SSH command and check for failures
run_ssh() {
    stdbuf -oL -eL $SSH_CMD 2>&1 | while IFS= read -r line
    do
        echo "$line"
        if [[ "$line" == *"remote port forwarding failed for listen port"* ]]; then
            echo "SSH remote port forwarding failed. Exiting..."
            pkill -P $$ ssh  # Kill the SSH command
            return 1
        fi
    done
    return 0
}

# This script is run from boge

while true
do
	echo "Check if we can resolve URL"

	hostname_to_resolve="icehack.asuscomm.com"
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
	
	if run_ssh; then
        echo "SSH tunnel established successfully."
    else
        echo "Retrying SSH command..."
    fi

	echo "Tunnle failed, sleep 1 minute and try again"
	sleep 55
	echo "Starting again in 5 sec"
	sleep 5
done