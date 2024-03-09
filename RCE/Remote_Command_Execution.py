import winrm
import sys

# Function to print help commands
def print_help():
    print("\nAvailable commands:")
    print("  - 'exit' : Exit the interactive shell")
    print("  - 'help' : Display this help message")
    print("  - '<PowerShell Command>' : Execute the given PowerShell command")
    print()

# Function to handle execution of PowerShell commands
def execute_command(session, cmd):
    # Suppressing the progress stream to avoid CLIXML output
    ps_script = f"$ProgressPreference = 'SilentlyContinue'; {cmd}"
    result = session.run_ps(ps_script)
    print(f"\nResponse code: {result.status_code}")
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
            cmd = input("PS> ").strip()
            if cmd.lower() == 'exit':
                print("Exiting interactive shell.")
                break
            elif cmd.lower() == 'help':
                print_help()
            else:
                execute_command(session, cmd)

        except KeyboardInterrupt:
            print("\nSession interrupted by user.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

except Exception as e:
    print(f"Failed to connect to {host}: {e}")
    sys.exit(1)
