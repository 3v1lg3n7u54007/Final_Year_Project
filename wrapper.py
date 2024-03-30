import os
import json
import subprocess
import os.path as directoryPath

def banner():
    print(
        """\n
      .o.         .oooooo.   ooooooooooooo ooooo oooooo     oooo oooooooooooo      oooooooooo.   ooooo ooooooooo.   oooooooooooo   .oooooo.   ooooooooooooo   .oooooo.   ooooooooo.   oooooo   oooo      ooooooo  ooooo 
     .888.       d8P'  `Y8b  8'   888   `8 `888'  `888.     .8'  `888'     `8      `888'   `Y8b  `888' `888   `Y88. `888'     `8  d8P'  `Y8b  8'   888   `8  d8P'  `Y8b  `888   `Y88.  `888.   .8'        `8888    d8'  
    .8"888.     888               888       888    `888.   .8'    888               888      888  888   888   .d88'  888         888               888      888      888  888   .d88'   `888. .8'           Y888..8P    
   .8' `888.    888               888       888     `888. .8'     888oooo8          888      888  888   888ooo88P'   888oooo8    888               888      888      888  888ooo88P'     `888.8'             `8888'     
  .88ooo8888.   888               888       888      `888.8'      888    "          888      888  888   888`88b.     888    "    888               888      888      888  888`88b.        `888'             .8PY888.    
 .8'     `888.  `88b    ooo       888       888       `888'       888       o       888     d88'  888   888  `88b.   888       o `88b    ooo       888      `88b    d88'  888  `88b.       888             d8'  `888b   
o88o     o8888o  `Y8bood8P'      o888o     o888o       `8'       o888ooooood8      o888bood8P'   o888o o888o  o888o o888ooooood8  `Y8bood8P'      o888o      `Y8bood8P'  o888o  o888o     o888o          o888o  o88888o                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
"""
    )

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
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print(f"Server started on port {port} in the background.")
            return process
        except Exception as e:
            print(f"Failed to start the server on port {port}: {e}")
            return None

    if start:
        kill_server()
        return start_server()
    else:
        return kill_server()


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


if __name__ == "__main__":

    server_process = None

    try:
        ENV = load_environment()

        # Start the server
        server_process = manage_server(1231, start=True)

        getUserInput(ENV)

    except KeyboardInterrupt:
        print("\nDetected Ctrl+C. Shutting down server and exiting gracefully...")

        if server_process is not None:
            manage_server(1231, start=False)

    except Exception as error:
        print(f"An unexpected error occurred: {error}")

    finally:
        if server_process is not None:
            manage_server(1231, start=False)

        print("Exiting gracefully...")
