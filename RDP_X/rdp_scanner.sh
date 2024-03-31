#!/bin/bash

echo "$(<./ascii2.txt )"

# Function to check RDP port for an individual host
check_rdp_port() {
    local host=$1
    if nc -zvw1 "$host" "$rdp_port" &>/dev/null; then
        echo -e "\e[32mRDP is enabled on $host\e[0m"
        echo "$host" >> activeRDPs.txt
    fi
}

echo "--[ TOOL ]--[ RDP SCANNER ]--[ SUJAL TULADHAR ]"

# Prompt the user for subnet (N) or single IP (H)
choice=$(zenity --list --title="Scan Type" --column="Type" "Network" "Host" --text="Please specify the scan type you want to perform. [Network or Host based]")

if [[ $choice == "Network" ]]; then
    valid_input=false

    while [[ $valid_input == false ]]; do
        # Prompt the user for the network range using Zenity
        network_range=$(zenity --entry --title="Network Scanner" --text="Enter the network range (Example: 192.168.15.0):")

        # Validate the input with an enhanced regex that checks for valid IPv4 addresses
        if [[ ! $network_range =~ ^([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$ ]]; then
            zenity --error --text="Invalid network range format. Please enter a valid IP address."
        else
            valid_input=true
        fi
    done

    # Specify the RDP port
    rdp_port=3389

    # Extract the network prefix (e.g., 192.168.1)
    network_prefix="${network_range%.*}"

    # Function to display scanning message
    display_scanning_message() {
        echo "Scanning the network..."
    }

    echo "" > activeRDPs.txt

    # Run the scanning message display
    display_scanning_message

    # Check RDP port for each host in the specified range in the background
    for host in "$network_prefix".{1..254}; do
        check_rdp_port "$host" &
    done

    # Sleep for 15 seconds to allow some scans to complete
    sleep 15

    # End the program
    echo "Scanning complete."
    
    ./rdp_bruteforce.sh

elif [[ $choice == "Host" ]]; then
    valid_input=false

    while [[ $valid_input == false ]]; do
        # Prompt the user for a single IP address
        host_ip=$(zenity --entry --title="Host Scanner" --text="Enter the host IP address (Example: 192.168.15.X):")

        # Validate the input with an enhanced regex that checks for valid IPv4 addresses
        if [[ ! $host_ip =~ ^([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$ ]]; then
            zenity --error --text="Invalid IP address format. Please enter a valid IP address."
        else
            valid_input=true
        fi
    done

    # Check RDP port for the specified host
    check_rdp_port "$host_ip"

    # Rewrite the content of activeRDPs.txt
    echo "$host_ip" > activeRDPs.txt

    # Invoke rdp_bruteforce.sh script
    ./rdp_bruteforce.sh

    # No need to exit here if you want the script to potentially continue or end naturally
else
    zenity --error --text="Invalid choice. Please select either 'N' or 'H'."
    exit 1
fi

