#!/bin/bash

echo "


  _____  _____  _______   __
 |  __ \|  __ \|  __ \ \ / /
 | |__) | |  | | |__) \ V / 
 |  _  /| |  | |  ___/ > <  
 | | \ \| |__| | |    / . \ 
 |_|  \_\_____/|_|   /_/ \_\
                            
                            
"

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

if [[ $choice == "N" ]]; then
    # Prompt the user for the network range using Zenity
    network_range=$(zenity --entry --title="Network Scanner" --text="Enter the network range (e.g., 192.168.15.0):")

    # Validate the input
    if [[ ! $network_range =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        zenity --error --text="Invalid network range format. Please enter a valid IP address."
        exit 1
    fi

    # Specify the RDP port
    rdp_port=3389

    # Extract the network prefix (e.g., 192.168.15)
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

    # Sleep for 30 seconds
    sleep 30

    # End the program
    echo "Scanning complete."
    
    ./rdp_bruteforce.sh

elif [[ $choice == "H" ]]; then
    # Prompt the user for a single IP address
    host_ip=$(zenity --entry --title="Host Scanner" --text="Enter the host IP address:")
    
    # Validate the input
    if [[ ! $host_ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        zenity --error --text="Invalid IP address format. Please enter a valid IP address."
        exit 1
    fi

    # Check RDP port for the specified host
    check_rdp_port "$host_ip"

    # Rewrite the content of activeRDPs.txt
    echo "$host_ip" > activeRDPs.txt

    # Invoke rdp_bruteforce.sh script
    ./rdp_bruteforce.sh

    exit 0
else
    zenity --error --text="Invalid choice. Please select either 'N' or 'H'."
    exit 1
fi
