from dotenv import load_dotenv
import os
import subprocess
import csv
from openai import OpenAI

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)  # Replace with your actual API key

def run_build_bat():
    """
    Executes the `build.bat` file located in the `compile_project` directory using the MSYS2 shell.

    Parameters:
    - None

    Returns:
    - None
    """
    # Save the initial working directory
    initial_directory = os.getcwd()

    # Relative path to the 'compile_project' directory
    build_directory = os.path.join(initial_directory, 'compile_project')

    # Path to the batch file (build.bat) within the relative directory
    build_bat = os.path.join(build_directory, 'build.bat')

    try:
        # Change the current working directory to the relative 'compile_project' directory
        os.chdir(build_directory)

        # Execute the batch file using subprocess
        process = subprocess.Popen([build_bat], shell=True)
        
        # Wait for the batch process to complete
        process.wait()

    finally:
        # After the process is done, navigate back to the initial directory
        os.chdir(initial_directory)



def run_renode_script():
    """
    Executes a Renode simulation script to run the simulation and generate a CSV file with the results.

    Parameters:
    - None

    Returns:
    - None
    """

    print("\n--- Phase 5: Renode-Validation ---")
    
    # Assuming the current working directory is Paper_Codegeneration
    current_dir = os.getcwd()  # Get the current directory (Paper_CodeGeneration)

    # Define relative paths based on the current directory
    renode_script_path = os.path.join(current_dir, 'run_simulation_script.resc')
    elf_file_path = os.path.join(current_dir, 'compile_project/build/src/STM32F4Template.elf')
    csv_output_path = os.path.join(current_dir, 'results/simulation_test.csv')

    # Write the Renode script to a file with relative paths
    renode_script_content = f"""
    mach create
    machine LoadPlatformDescription @platforms/boards/stm32f4_discovery-kit.repl
    sysbus LoadELF "{elf_file_path}"

    # Set log level to capture messages for USART2
    logLevel -1 sysbus.usart2

    # Record USART2 output directly to a CSV file
    sysbus.usart2 CreateFileBackend @{csv_output_path}
    showAnalyzer sysbus.usart2
    start

    # Pause for 5 seconds to let the simulation run before quitting
    sleep 5

    # Close Renode after the simulation
    quit
    """

    with open(renode_script_path, 'w') as renode_file:
        renode_file.write(renode_script_content)

    # Now run the Renode CLI with the script
    try:
        subprocess.run(["renode", renode_script_path], check=True)
        print("Renode script executed successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Failed to execute Renode script: {e}")


def read_and_delete_csv(file_path):
    """
    Reads a number from the first cell of a specified CSV file and deletes the file.

    Parameters:
    - file_path (str): Path to the CSV file.

    Returns:
    - str or None: The number read from the first cell of the CSV file, or `None` if the file is empty.
    """
    number = None
    # Read the number from the CSV
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row:  # If the row contains data
                number = row[0]
                break

    # Delete the file
    os.remove(file_path)

    return number
