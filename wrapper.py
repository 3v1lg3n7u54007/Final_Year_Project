import os
import json
import subprocess
import os.path as directoryPath
import time

def banner():
    return


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


def execute_script(command, script_path):
    """Executes the given script based on its file extension, ensuring correct relative paths."""
    # Change the current working directory to the script's folder
    original_cwd = os.getcwd()  # Save the original working directory
    script_folder = os.path.join(original_cwd, script_path)
    print(command, script_folder)

    try:
        os.chdir(script_folder)

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
            print(f"Unsupported script type for command: {command}")
            exit()
    except Exception as error:
        print(error) 
    finally:
        os.chdir(original_cwd)  # Change back to the original working directory


def load_environment():
    """Loads the environment configurations from a JSON file."""
    with open("env.json", "r") as envFile:
        ENVIRONMENT = json.load(envFile)
    return ENVIRONMENT["ENV"]


def display_environments(ENV):
    """Displays the available environments and their modes."""
    for env in ENV:
        print(f"{env['id']}. {env['name']}")
        if "modes" in env:
            for mode in env["modes"]:
                print(f"   - {mode['name']}: {mode['invokeCommand']}")
        else:
            print(f"   - Command: {env['invokeCommand']}")


def getUserInput(ENV):
    """Handles user interaction to choose a test and execution mode, with a check for OS compatibility."""
    clear_screen()
    print("\nSELECT TEST:")
    display_environments(ENV)

    env_id = int(input("\nInput Test ID >>> ").strip())
    selected_env = next((env for env in ENV if env["id"] == env_id), None)

    if not selected_env:
        print("\nInvalid Test Selected. Exiting...")
        exit()

    current_os = "nt" if os.name == "nt" else "linux"
    if selected_env["environment"] not in [current_os, "any"]:
        print(
            f"\nSelected environment is not compatible with the current OS ({current_os}). Exiting..."
        )
        exit()

    if "modes" in selected_env:
        print(f"\nSELECT MODE FOR {selected_env['name']}:")
        for index, mode in enumerate(selected_env["modes"], start=1):
            print(f"{index}. {mode['name']}")
        mode_index = int(input("\nInput Mode ID >>> ").strip()) - 1

        try:
            selected_mode = selected_env["modes"][mode_index]
            command = selected_mode["invokeCommand"]
            script_name = command.split()[-1]
            script_path = selected_env["folderPath"]
            print(f"\nExecuting {selected_mode['name']} mode command...")
            execute_script(script_name, script_path)

        except IndexError:
            print("\nInvalid Mode. Exiting...")
            exit()
    else:
        command = selected_env["invokeCommand"]
        script_name = command.split()[-1]
        script_path = selected_env["folderPath"]
        print(f"\nExecuting command for {selected_env['name']}...")
        execute_script(script_name, script_path)

def start_web_server():
    # Start the server as a subprocess without blocking
    # subprocess.Popen starts the process and returns immediately
    os.system("fuser -k 1231/tcp")
    command = ["python3", "-m", "http.server", "1231"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print("Server started on port 1231 in the background.")
    return process  # Returning the process allows you to interact with it later if needed

# To run the function
process = start_web_server()

# Load the environment configurations
ENV = load_environment()

# Example usage
#getUserInput(ENV)
