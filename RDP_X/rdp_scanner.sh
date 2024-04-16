#!/bin/bash
clear

echo "$(<./ascii2.txt)"

# Function to check RDP port for an individual host
check_rdp_port_network() {
    
    # Defining a local variable 'host' to store the IP address of the host being checked.
    local host=$1 

    # Using netcat (nc) to check if the RDP port is open on the specified host IP.
    if nc -zvw1 "$host" "$rdp_port" &>/dev/null; then 
        echo -e "\e[32mRDP is enabled on $host\e[0m"
        echo "$host" >> activeRDPs.txt
    fi
}

check_rdp_port_host() {
    local $host_ip=$1
    if nc -zvw1 "$host_ip" "$rdp_port" &>/dev/null; then
        zenity --info --text="Remote Desktop Protcol service is enabled on the host."
        echo "$host" >> activeRDPs.txt
    else 
        zenity --info --text="Remote Desktop Protocol service not enabled on the host."
        exit 1
    fi

}
    
# Function to check file existence
check_file_exists() {
    # If the file doesn't exist, prints an error message indicating the file was not found.
    if [ ! -f "$1" ]; then
        echo -e "\e[91m$2 file not found. Please check the file path.\e[0m"
    
    # If the file exists, prints a message indicating that the 'ActiveRDPs.txt' file was found and the process will proceed.
    else 
        echo -e "ActiveRDPs.txt File Found in the directory . . . Proceeding with the process"
    fi
}

echo "--[ TOOL ]--[ RDP SCANNER ]--[ SUJAL TULADHAR ]"

# Prompt the user for subnet (N) or single IP (H)
choice=$(zenity --list --title="Scan Type" --column="Type" "Network" "Host" --text="Please specify the scan type you want to perform. [Network or Host based]") 

if [[ $choice == "Network" ]]; then
    while true; do

        # Prompts the user for the network range using Zenity and captures the exit status.
        network_range=$(zenity --entry --title="Network Scanner" --text="Enter the network range (Example: 192.168.15.0):")
        exit_status=$?

        # Check if the user clicked the cancel button or closed the dialog
        if [[ $exit_status -ne 0 ]]; then
            zenity --info --text="Operation cancelled by user."
            exit 2
        fi

        # Validate the input with an enhanced regex that checks for valid IPv4 addresses
        if [[ $network_range =~ ^([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$ ]]; then

            # Specify the RDP port
            rdp_port=3389
        
            # Extract the network prefix (e.g., 192.168.1)
            network_prefix="${network_range%.*}"
        
            # Function to display scanning message
            display_scanning_message() {
                clear
                echo "Scanning the network for Remote Destop Protocol Service..."
            }
        
            echo "" > activeRDPs.txt
        
            # Run the scanning message display
            display_scanning_message
        
            # Check RDP port for each host in the specified range in the background
            for host in $(seq 1 254); do
                # Calls the function to check the RDP port for each host in the background.
                check_rdp_port_network "$network_prefix.$host" &
            done
        
            check_file_exists ./activeRDPs.txt

            # Sleep for 15 seconds to allow some scans to complete
            sleep 15
        
            # End the program
            echo "Scanning complete."
            
            # Invoke rdp_bruteforce.sh script
            ./rdp_bruteforce.sh
            break
        else
            zenity --error --text="Invalid network range format. Please enter a valid IP address."
        fi
    done

# If the user choice is "Host", enter a loop to continuously prompt the user for a single IP address.
elif [[ $choice == "Host" ]]; then
    while true; do

        # Prompts the user for a single IP address and captures the exit status.
        host_ip=$(zenity --entry --title="Host Scanner" --text="Enter the host IP address (Example: 192.168.15.X):")
        exit_status=$?

        # Check if the user clicked the cancel button or closed the dialog
        if [[ $exit_status -ne 0 ]]; then
            zenity --info --text="Operation cancelled by user."
            exit 2
        fi

        # Validate the input with an enhanced regex that checks for valid IPv4 addresses
        if [[ $host_ip =~ ^([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$ ]]; then

            # Specify the RDP port
            rdp_port=3389

            # Check RDP port for the specified host
            check_rdp_port_host "$host_ip"
        
            check_file_exists ./activeRDPs.txt
        
            # Invoke rdp_bruteforce.sh script
            ./rdp_bruteforce.sh
        
            break
        else
            zenity --error --text="Invalid IP address format. Please enter a valid IP address."
        fi
    done

else
    zenity --info --text="Operation cancelled by user."
fi
