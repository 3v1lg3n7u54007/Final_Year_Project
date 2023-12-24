import winrm

# Define target machine details
host = '192.168.15.145'
domain = 'Activedirectoryenvironment.local'
user = 'EAnderson'
password = 'Employee23213'

# Informative message about the connection being established
print(f"Connecting to {host} using NTLM authentication...")

# Create a winrm.Session object with NTLM authentication
session = winrm.Session(
    host,
    auth=(f'{domain}\\{user}', password),
    transport='ntlm',
    server_cert_validation='ignore'  # Use 'ignore' to bypass certificate validation
)

# Informative message about the PowerShell script to be executed
print(f"Executing PowerShell script on {host}...")

# Specify the PowerShell script to run
ps_script = 'pwd'

# Use run_ps method to execute PowerShell script
result = session.run_ps(ps_script)

# Informative message about the execution result
print("Execution Result:")
print("-" * 20)

# Print the result details
print(f"Response code: {result.status_code}")
print(f"\nStandard Output:\n{result.std_out.decode('utf-8')}")
print(f"\nError Output:\n{result.std_err.decode('utf-8')}")

# Informative message about the script execution completion
print("\nScript execution completed.")
