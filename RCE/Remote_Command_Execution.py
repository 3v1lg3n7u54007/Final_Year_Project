import winrm
import sys
import os

def banner():
    # ASCII art for visual appeal
    print("""
ooooooooo.     .oooooo.   oooooooooooo 
`888   `Y88.  d8P'  `Y8b  `888'     `8 
 888   .d88' 888           888         
 888ooo88P'  888           888oooo8    
 888`88b.    888           888    "    
 888  `88b.  `88b    ooo   888       o 
o888o  o888o  `Y8bood8P'  o888ooooood8 
                                                                                                                                                                          """)

# Function to print help commands
def print_help():
    print("\nAvailable commands:")
    print("  - 'exit' : Exit the interactive shell")
    print("  - 'help' : Display this help message")
    print("  - '<PowerShell Command>' : Execute the given PowerShell command")
    print()

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

clear_screen()

# Function to handle execution of PowerShell commands
def execute_command(session, cmd):

    # Suppressing the progress stream to avoid CLIXML output
    ps_script = f"$ProgressPreference = 'SilentlyContinue'; {cmd}"
    result = session.run_ps(ps_script)

    #print(f"\nResponse code: {result.status_code}")
    print(f"Standard Output:\n{result.std_out.decode('utf-8')}")
    if result.std_err:
        print(f"Error Output:\n{result.std_err.decode('utf-8')}")

# Define target machine details
host = '192.168.15.170'
domain = 'Activedirectoryenvironment.local'
user = 'EAnderson'
password = 'Employee23213'

try:
    # Create a winrm.Session object with NTLM authentication
    session = winrm.Session(
        host,
        auth=(f'{domain}\\{user}', password),
        transport='ntlm',
        server_cert_validation='ignore'
    )

    # Informative message about the connection being established
    print(f"Connected to {host}. Enter PowerShell commands to execute (type 'exit' to quit):")
    print_help()

    # Interactive shell loop
    while True:
        try:
            # Prompt the user for input and strip leading/trailing whitespace
            cmd = input("PS> ").strip()

            # If the user enters 'exit', terminate the loop and exit the shell
            if cmd.lower() == 'exit':
                print("Exiting interactive shell.")
                break

            # If the user enters 'help', display the help message
            elif cmd.lower() == 'help':
                print_help()
            
            # Otherwise, execute the entered PowerShell command
            else:
                execute_command(session, cmd)

        # If the user interrupts the session (e.g., with Ctrl+C), handle the interruption gracefully
        except KeyboardInterrupt:
            print("\nSession interrupted by user.")
            break

        # Handle other exceptions (e.g., connection errors, command execution errors)
        except Exception as e:
            print(f"An error occurred: {e}")

# Handle exceptions related to connection errors
except Exception as e:
    print(f"Failed to connect to {host}: {e}")
    sys.exit(1)
