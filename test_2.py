from implementation.rag import process_c_files
from implementation.code_generation import fix_c_code
from implementation.concatenate_code import concatenate_file
from implementation.test_functions import clear_all_files, compile_code
from dotenv import load_dotenv
import os
import time
import json
import uuid
from datetime import datetime
from implementation.code_validation import run_build_bat, run_renode_script, read_and_delete_csv


load_dotenv()  # Load environment variables from .env file


"""
This script contains the function 'run_iterations_without_interface' which automates the process of fixing,
compiling, and simulating C code over multiple iterations. The results are logged into a JSON file with unique entries for each iteration.
"""

def run_iterations_without_interface(num_iterations):
    """
    Executes the process of fixing, compiling, and simulating C code iteratively 
    for a specified number of iterations without a user interface.

    Parameters:
    - num_iterations (int): The number of iterations to run.

    Returns:
    - None: Results are saved to the JSON file `results/test_data_2.json`.

    Example usage:
    ```
    run_iterations_without_interface(10)
    ```
    """

    json_file_path = 'results/test_data_2.json'
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
        functioning_code_binary = read_and_delete_csv(csv_file_path)


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
