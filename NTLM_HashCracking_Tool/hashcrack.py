import os
import re
import hashlib
import time

# Function to print a styled banner
def banner():
    print(
        """\n
ooooo      ooo ooooooooooooo ooooo        ooo        ooooo      ooooo   ooooo       .o.        .oooooo..o ooooo   ooooo   .oooooo.   ooooooooo.         .o.         .oooooo.   oooo    oooo 
`888b.     `8' 8'   888   `8 `888'        `88.       .888'      `888'   `888'      .888.      d8P'    `Y8 `888'   `888'  d8P'  `Y8b  `888   `Y88.      .888.       d8P'  `Y8b  `888   .8P'  
 8 `88b.    8       888       888          888b     d'888        888     888      .8"888.     Y88bo.       888     888  888           888   .d88'     .8"888.     888           888  d8'    
 8   `88b.  8       888       888          8 Y88. .P  888        888ooooo888     .8' `888.     `"Y8888o.   888ooooo888  888           888ooo88P'     .8' `888.    888           88888[      
 8     `88b.8       888       888          8  `888'   888        888     888    .88ooo8888.        `"Y88b  888     888  888           888`88b.      .88ooo8888.   888           888`88b.    
 8       `888       888       888       o  8    Y     888        888     888   .8'     `888.  oo     .d8P  888     888  `88b    ooo   888  `88b.   .8'     `888.  `88b    ooo   888  `88b.  
o8o        `8      o888o     o888ooooood8 o8o        o888o      o888o   o888o o88o     o8888o 8""88888P'  o888o   o888o  `Y8bood8P'  o888o  o888o o88o     o8888o  `Y8bood8P'  o888o  o888o 
                                                                                                                                                                                            
                                                                                                                                                                                            
                                                                                                                                                                                            
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

with open('cracked_hash.txt', 'a') as file:
    if crackedPassword == "":
        output_message = "\n--[ RESULT ]--[ No Hashes Cracked ]\n"
        print(output_message)
        file.write(output_message)
    else:
        output_message = f"\n--[ RESULT ]--[ {count} Passwords Cracked Successfully ]\n"
        print(output_message)
        file.write(output_message)
        for value in crackedPassword:
            del value["NTLMhash"]
           
            output_line = f"{value}\n"
            print(output_line.strip()) # strip() to remove the extra newline when printing
            file.write(output_line)


time.sleep(5)
