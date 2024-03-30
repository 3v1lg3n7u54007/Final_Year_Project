import os
import re
import hashlib

# Function to print a styled banner
def banner():
    print(
        """\n
███╗   ██╗████████╗██╗     ███╗   ███╗    ██╗  ██╗ █████╗ ███████╗██╗  ██╗ ██████╗██████╗  █████╗  ██████╗██╗  ██╗
████╗  ██║╚══██╔══╝██║     ████╗ ████║    ██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
██╔██╗ ██║   ██║   ██║     ██╔████╔██║    ███████║███████║███████╗███████║██║     ██████╔╝███████║██║     █████╔╝ 
██║╚██╗██║   ██║   ██║     ██║╚██╔╝██║    ██╔══██║██╔══██║╚════██║██╔══██║██║     ██╔══██╗██╔══██║██║     ██╔═██╗ 
██║ ╚████║   ██║   ███████╗██║ ╚═╝ ██║    ██║  ██║██║  ██║███████║██║  ██║╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗
╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝     ╚═╝    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
"""
    )


# Getting passwords for cracking hashes...
passwordFile = "passwords.txt"
with open(passwordFile, "r") as file:
    passwords = file.readlines()
    passwords = [value.replace("\n", "") for value in passwords]

if len(passwords) == 0:
    print("--[ ERROR ]--[ Passwords.txt is empty ]")
    exit()


# Function to generate an NTLM hash from the input string
def create_ntlm_hash(input_string):
    return hashlib.new("md4", input_string.encode("utf-16le")).hexdigest()


# Function to compare two hash values and return True if they match
def crack(hashValue, testValue):
    if hashValue == testValue:
        return True


# Function to clear the terminal screen and reprint the banner
def clear_screen():
    # Clear command for Windows
    if os.name == "nt":
        _ = os.system("cls")

    # Clear command for Unix/Linux/Mac
    else:
        _ = os.system("clear")

    # Reprint the banner after clearing
    banner()


# Function to extract NTLM hashes from a file with specific format
def getNTLMHashesFromFile():
    # Regular expression pattern to extract the NTLM hashes
    pattern = r"^([^:]+):(\d+):([a-fA-F0-9]{32}):([a-fA-F0-9]{32}):::$"

    try:
        # Open the file containing the hashes
        with open("rawdump.txt", "r", encoding="utf-8") as file:
            rawdata = file.readlines()
            rawdata = [value.replace("\n", "").strip() for value in rawdata]

        NTLMHashes = []

        # Parse each line with the regex pattern to extract the hashes
        for hash in rawdata:
            match = re.match(pattern, hash)

            if match:
                # Extract username, RID, and NTLM hash
                username = match.group(1)
                RID = match.group(2)
                # LMhash = match.group(3)
                NTLMhash = match.group(4)

                # Append extracted data as a dictionary to NTLMHashes list
                NTLMHashes.append(
                    {
                        "username": username,
                        "RID": RID,
                        "NTLMhash": NTLMhash,
                        "Password": "",
                    }
                )

        return NTLMHashes

    except Exception as error:
        # Print error message if unable to read or parse the file
        print(f"--[ ERROR ]--[ RAW DATA EXTRACTION ERROR ]--[ {error} ]")
        exit()


# Function to get user input for selecting hash input method
def getUserInput():
    message = None
    while True:
        clear_screen()
        print("\n1. Load Hashes From File")
        print("\n2. Load Hashes Manually")
        if message:
            print(f"\n--[ INFO ]--[ {message} ]")

        inputChoice = input("\nCHOOSE (1 or 2) >>> ").strip()

        if inputChoice in ["1", "2"]:

            if inputChoice == "2":
                hashValue = input("\nEnter Hash Value >>> ").strip()
                return [
                    {"username": "", "RID": "", "NTLMhash": hashValue, "Password": ""}
                ]

            else:
                # Load hashes from file
                return getNTLMHashesFromFile()

        else:
            message = "INVALID OPTION SELECTED"
            continue


# DRIVER CODE...
print("--[ INFO ]--[ EXTRACTED DATA ]")

NTLMHashes = getUserInput()
for value in NTLMHashes:
    print(f"{value}")

print("\n--[ INFO ]--[ CRACKING PASSWORDS ]", end="")

crackedPassword = []
count = 0

for hash in NTLMHashes:
    for index, value in enumerate(passwords):

        testvalue = create_ntlm_hash(value)

        if crack(hash["NTLMhash"], testvalue):
            hash["Password"] = value
            crackedPassword.append(hash)
            count += 1
            break

if crackedPassword == "":
    print("\n--[ RESULT ]--[ No Hashes Cracked ]")

else:
    print(f"\n--[ RESULT ]--[ {count} Passwords Cracked Successfully ]")

    for value in crackedPassword:
        del value["NTLMhash"]
        print(f"{value}")
