from implementation.helper_functions.rag import process_c_files
from implementation.hypothesis_3_2 import fix_c_code
from interface_3 import concatenate_file
from implementation.test_functions import clear_all_files, compile_code
from dotenv import load_dotenv
import os
import subprocess
import time
import json
import uuid
from datetime import datetime
import csv
from run_similarity import run_similarity

load_dotenv()  # Load environment variables from .env file


def run_build_bat():
    """
    Runs the build.bat file from the correct working directory using MSYS2 shell.
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
    Runs the Renode script to execute the simulation and generate the CSV file.
    """
    renode_script_path = r'C:\msys64\Paper_CodeGeneration\run_simulation_script.resc'
    
    # Write the Renode script to a file
    renode_script_content = """
    mach create
    machine LoadPlatformDescription @platforms/boards/stm32f4_discovery-kit.repl
    sysbus LoadELF "C:/msys64/Paper_CodeGeneration/compile_project/build/src/STM32F4Template.elf"
    
    # Set log level to capture messages for USART2
    logLevel -1 sysbus.usart2
    
    # Record USART2 output directly to a CSV file
    sysbus.usart2 CreateFileBackend @C:/msys64/Paper_CodeGeneration/results/simulation_test.csv
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

        
def read_and_clear_csv(file_path):
    """
    Reads a number from the given CSV file and erases its content.
    Assumes the number is stored in the first cell of the CSV.
    """
    number = None
    # Read the number from the CSV
    with open(file_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if row:  # If the row contains data
                number = row[0]
                break

    # Erase the content of the file
    with open(file_path, 'w') as csvfile:
        csvfile.write("")

    return number

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")


def run_iterations_without_interface(num_iterations):
    """
    Runs the iteration process without the interface for a specified number of times.
    Logs the results into a JSON file with unique entries for each iteration.
    """

    json_file_path = 'results/test_data_3_2.json'
    csv_file_path = 'results/simulation_test.csv'

    # Check if the JSON file exists, if not create it with initial structure
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            test_data = json.load(json_file)
    else:
        test_data = {"test_data_3_2": []}

    for i in range(num_iterations):
        state = {'iteration': 0, 'total_time': 0.0}

        # Start the timer for the iteration
        start_time = time.time()

        while state['iteration'] < 15:
            process_c_files(r"compile_project\src")

            source_code_path = r'compile_project\src\main.c'

            fixed_code = fix_c_code(source_code_path)

            state['iteration'] += 1
            print(f"######################Iteration {state['iteration']}####################################")

            if not fixed_code:
                break

        # Calculate total elapsed time
        elapsed_time = time.time() - start_time
        state['total_time'] = elapsed_time

        # Compile the final code
        compilation_success = compile_code(source_code_path)

        # Create a unique ID and timestamp for the new entry
        unique_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()


        # Run the build.bat file
        run_build_bat()

        # Run the Renode simulation
        run_renode_script()

        # Read the Functioning code binary from the CSV and clear the file
        functioning_code_binary = read_and_clear_csv(csv_file_path)


        # Prepare the new entry
        new_entry = {
            "unique_id": unique_id,
            "timestamp": timestamp,
            "total time (seconds)": state['total_time'],
            "compilation-success": compilation_success,
            "Functioning code Binary": functioning_code_binary,
            "Code": concatenate_file()
        }

        # Append the new entry to the test data
        test_data["test_data_3_2"].append(new_entry)

        print(f"Test Iteration {i + 1} finished")

        # Clear all files after each run
        clear_all_files()

        # Write the updated data back to the JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(test_data, json_file, indent=4)

    print(f"Completed {num_iterations} iterations. Results saved to {json_file_path}.")

# reset everything to ensure working code
clear_all_files()
process_c_files(r"compile_project\src")
source_code_path = r'compile_project\src\main.c'

fixed_code = fix_c_code(source_code_path)

# Run the iteration process 10 times
run_iterations_without_interface(1)

run_similarity()