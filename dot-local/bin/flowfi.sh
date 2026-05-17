#!/bin/bash

# Load secrets
source /home/szahem/.secrets
PORT=8004

# Default configuration variables
COUNT=1
IS_LOOP=0
LOOP_DELAY=1

# Function to display usage information
usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -p --port   <number>    Modify the port."
    echo "  -c --count	<number>     	Post the request <number> times."
    echo "  -l --loop	<seconds>	Post the request indefinitely, waiting <seconds> in between."
    echo "  -s --silent    		Suppress all outputs, including errors."
    echo "  -h, --help       		Display this usage info."
    exit 1
}

# Function to send the actual request
send_request() {
    echo "Sending request to citiez.."
    URL="http://10.28.47.254:$PORT/index.php?zone=citiez"
    # Note: Added '-s' to curl to suppress its default progress meter
    curl -s -L -X POST "$URL" -K <(cat <<EOF
data-urlencode "auth_user=$UNIVERSITY_EMAIL"
data-urlencode "auth_pass=$UNIVERSITY_PASSWORD"
data "accept=Login"
EOF
    ) --connect-timeout 7 | echo
}

# If no arguments are provided, show usage and exit
if [[ "$#" -eq 0 ]]; then
    usage
fi

# Parse command-line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
	    -p|--port)
            if [[ ! "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: -c requires a valid number."
                exit 1
            fi
            PORT="$2"
            shift 2
            ;;
        -c|--count)
            if [[ ! "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: -c requires a valid number."
                exit 1
            fi
            COUNT="$2"
            shift 2
            ;;
        -l|--loop)
            if [[ ! "$2" =~ ^[0-9]+$ ]]; then
                echo "Error: --loop requires a valid number of seconds."
                exit 1
            fi
            IS_LOOP=1
            LOOP_DELAY="$2"
            shift 2
            ;;
        -s|--silent)
            # Redirect all standard output and standard error to /dev/null globally
            exec >/dev/null 2>&1
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Unknown parameter passed: $1"
            usage
            ;;
    esac
done

# Execution Logic
if [[ $IS_LOOP -eq 1 ]]; then
    # Infinite loop behavior
    while true; do
        send_request
        sleep "$LOOP_DELAY"
    done
else
    # Defined count behavior (defaults to 1 if just --silent is passed)
    for ((i=1; i<=COUNT; i++)); do
        send_request
    done
fi
