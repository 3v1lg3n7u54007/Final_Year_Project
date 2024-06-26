import os
import json
import time
import subprocess
import os.path as directoryPath
import sys

def banner():
    RED   = '\033[91m'
    WHITE = '\033[97m'
    END   = '\033[0m'
    print(WHITE + """
      .o.         .oooooo.   ooooooooooooo ooooo oooooo     oooo oooooooooooo      oooooooooo.   ooooo ooooooooo.   oooooooooooo   .oooooo.   ooooooooooooo   .oooooo.   ooooooooo.   oooooo   oooo      ooooooo  ooooo 
     .888.       d8P'  `Y8b  8'   888   `8 `888'  `888.     .8'  `888'     `8      `888'   `Y8b  `888' `888   `Y88. `888'     `8  d8P'  `Y8b  8'   888   `8  d8P'  `Y8b  `888   `Y88.  `888.   .8'        `8888    d8'  
    .8"888.     888               888       888    `888.   .8'    888               888      888  888   888   .d88'  888         888               888      888      888  888   .d88'   `888. .8'           Y888..8P    
   .8' `888.    888               888       888     `888. .8'     888oooo8          888      888  888   888ooo88P'   888oooo8    888               888      888      888  888ooo88P'     `888.8'             `8888'     
  .88ooo8888.   888               888       888      `888.8'      888    "          888      888  888   888`88b.     888    "    888               888      888      888  888`88b.        `888'             .8PY888.    
 .8'     `888.  `88b    ooo       888       888       `888'       888       o       888     d88'  888   888  `88b.   888       o `88b    ooo       888      `88b    d88'  888  `88b.       888             d8'  `888b   
o88o     o8888o  `Y8bood8P'      o888o     o888o       `8'       o888ooooood8      o888bood8P'   o888o o888o  o888o o888ooooood8  `Y8bood8P'      o888o      `Y8bood8P'  o888o  o888o     o888o          o888o  o88888o 
""" + RED + "\n Use this tool within legal and ethical boundaries only. Unauthorized testing against Active Directory environments without explicit permission is prohibited.\n" + END )


def banner1():
    print("test")

def getFullPath(pathValue):
    """Converts a relative path to an absolute, normalized path."""
    return directoryPath.normpath(directoryPath.abspath(pathValue))


def clear_screen():
    """Clears the terminal screen, and prints a banner."""
    # For Windows
    if os.name == "nt":
        _ = os.system("cls")
    # For Linux and Mac
    else:
        _ = os.system("clear")

    banner()


def manage_server(port, start=True):
    """
    Manages a simple HTTP server on the specified port.

    Parameters:
    - port: The port number to use for the server.
    - start: Boolean indicating whether to start (True) or stop (False) the server.
    """

    def kill_server():
        """Kills any server running on the specified port."""
        try:
            # Use subprocess to execute the fuser command to kill the process on the specified port
            subprocess.check_output(["fuser", "-k", f"{port}/tcp"])
            print(f"Successfully killed process on port {port}.")
            return None

        except subprocess.CalledProcessError:
            print(f"No process was running on port {port}, or lack permissions.")

        except Exception as e:
            print(
                f"An error occurred while trying to kill the server on port {port}: {e}"
            )

    def start_server():
        """Starts the server on the specified port."""
        command = ["python", "-m", "http.server", str(port)]
        try:
            # Use subprocess.Popen to start the server process with the specified command
            process = subprocess.Popen(
                # Command to start the server
                command,

                # Redirect standard output to a pipe
                stdout=subprocess.PIPE,

                # Redirect standard error to a pipe
                stderr=subprocess.PIPE,
            )
            print(f"Server started on port {port} in the background.")
            return process
        except Exception as e:
            print(f"Failed to start the server on port {port}: {e}")
            return None

    if start:
        
        # If start is True, kill any existing server and start a new one
        # Kill any existing server running on the specified port
        kill_server()

        # Start a new server and return the process object
        return start_server()
    
    else:

        # If start is False, simply kill any existing server
        # Kill any existing server running on the specified port
        return kill_server()


def execute_script(command, script_path):
    """Executes the given script based on its file extension, ensuring correct relative paths."""
    # Change the current working directory to the script's folder
    original_cwd = os.getcwd()  # Save the original working directory

    # Concatenate the original working directory with the script path to form the full path to the script file
    script_folder = os.path.join(original_cwd, script_path)
    print(command, script_folder)

    try:
        # Attempt to change the current working directory to the script's folder
        os.chdir(script_folder)

        # Determine the script type based on its file extension and execute it accordingly
        if command.endswith(".py"):
            subprocess.run(["python", command])
        elif command.endswith(".sh"):
            subprocess.run(["bash", command])
        elif command.endswith(".ps1"):
            subprocess.run(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", command],
                shell=True,
            )
        else:
            raise Exception(f"Unsupported script type for command: {command}")

    # Catch subprocess errors and other exceptions
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error executing script: {e}")
    except Exception as error:
        raise Exception(f"An unexpected error occurred: {error}")
    
    # Ensure the working directory is reverted back to the original one regardless of exceptions
    finally:
        os.chdir(original_cwd)  # Change back to the original working directory


def load_environment():
    """Loads the environment configurations from a JSON file."""

    # Open the JSON file containing environment configurations in read mode
    with open("env.json", "r") as envFile:
        
        # Load the JSON data from the file
        ENVIRONMENT = json.load(envFile)
    
    # Return the value corresponding to the key "ENV" in the loaded JSON data
    return ENVIRONMENT["ENV"]


def display_environments(ENV):
    """Displays the available environments and their modes."""

    # Iterate over each environment in the provided ENV list
    for env in ENV:
        print(f"{env['id']}. {env['name']}")

        # Check if the environment has modes
        if "modes" in env:
            # Iterate over each mode in the environment
            for mode in env["modes"]:
                print(f"   - {mode['name']}: {mode['invokeCommand']}")
        else:
            print(f"   - Command: {env['invokeCommand']}")


def getUserInput(ENV):
    """Handles user interaction with Zenity dialogs for test and mode selection."""
    try:
       
        # Prepare the test selection dialog
        tests = "\n".join(f"{env['id']}. {env['name']}" for env in ENV)
        zenity_test_cmd = f"""bash -c "zenity --list --title='Select Test' --column='Test Case' --height=400 --width=400 --print-column=1 <<< '{tests}'" """
        
        # Execute the Zenity command and capture the selected test ID
        selected_test_id = subprocess.check_output(
            zenity_test_cmd, shell=True, text=True, stderr=subprocess.DEVNULL
        ).strip()

        # Check if a test was selected
        if not selected_test_id:
            raise Exception("No Test Selected. Exiting...")

        # Extract the selected test ID
        selected_test_id = int(
            selected_test_id.split(".")[0]
        )  # Extracting ID from selection
        
        # Find the selected environment based on the test ID
        selected_env = next((env for env in ENV if env["id"] == selected_test_id), None)

        # Determine the current operating system (OS)
        current_os = "nt" if os.name == "nt" else "linux"

        # Check if the selected environment's compatibility matches the current OS or is set to "any"
        if selected_env["environment"] not in [current_os, "any"]:
            raise Exception(
                f"\nSelected module is not compatible with the current OS ({current_os})"
            )

        # Check if the selected environment has different modes
        if "modes" in selected_env:

            # Prepare a formatted string containing the modes for selection
            modes = "\n".join(
                f"{index} {mode['name']}"
                for index, mode in enumerate(selected_env["modes"], start=1)
            )

            zenity_mode_cmd = f"zenity --list --title='Select Mode for {selected_env['name']}' --column='ID' --column='Mode' --height=200 --width=400 --print-column=1 <<< \"{modes}\""
            
            # Run the Zenity command to get the selected mode ID
            selected_mode_id = subprocess.check_output(
                zenity_mode_cmd, shell=True, text=True, stderr=subprocess.DEVNULL
            ).strip()

            # Convert the selected mode ID to an integer
            selected_mode_id = int(selected_mode_id) - 1

            # Retrieve the details of the selected mode
            selected_mode = selected_env["modes"][selected_mode_id]

            # Get the command associated with the selected mode
            command = selected_mode["invokeCommand"]

        else:
            # If no modes are available, use the default command for the selected environment
            command = selected_env["invokeCommand"]
        
        # Extract the script name from the command
        script_name = command.split()[-1]

        # Get the folder path where the script is located
        script_path = selected_env["folderPath"]
        print(f"\nExecuting command for {selected_env['name']}...")

        # Execute the script with the specified name and folder path
        execute_script(script_name, script_path)

    except subprocess.CalledProcessError as e:
        
        zenity_exit_cmd = "zenity --question --text='Do you want to close the tool?' --title='Confirm Exit'"
        try:
            # Execute the Zenity command and check the user's response
            subprocess.run(zenity_exit_cmd, shell=True, check=True, text=True, stderr=subprocess.DEVNULL)

            # If the user clicks "Yes", the program will exit here
            sys.exit(0)
            
        except subprocess.CalledProcessError:
            # If the user clicks "No", it throws a CalledProcessError and the program continues
            print("Continuing execution...")

if __name__ == "__main__":

    # Start the server outside the loop
    server_process = manage_server(
        1231, start=True
    )  

    while True:
        try:
            # Load environment configurations
            ENV = load_environment()
            clear_screen()

            # Handle user input for test and mode selection
            getUserInput(ENV)

            # Assuming successful completion, break the loop
            print("Operation completed successfully.")

        except KeyboardInterrupt:
            # Exit the loop if Ctrl+C is pressed
            print("\nDetected Ctrl+C. Exiting gracefully...")
            break  

        except Exception as error:
            # print(f"An unexpected error occurred: {error}")
            zenity_test_cmd = f"""bash -c 'zenity --error --text="{error}" --height=200 --width=400 '"""

            selected_test_id = subprocess.check_output(
                zenity_test_cmd, shell=True, text=True, stderr=subprocess.DEVNULL
            ).strip()

            # Check if the error message indicates an exit request
            if "Exiting" in str(error):
                exit()
            else:
                print("Attempting to restart...")
                time.sleep(1)  # Brief pause before restarting

    # Shutdown server process when exiting the loop
    if server_process is not None:
        manage_server(1231, start=False)
    print("Exiting gracefully...")
