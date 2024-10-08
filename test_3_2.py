import csv
import time
from implementation.helper_functions.rag import process_c_files
from implementation.hypothesis_3_2 import fix_c_code
from implementation.test_functions import clear_all_files, compile_code
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")


def run_iterations_without_interface(num_iterations):
    """
    Runs the iteration process without the interface for a specified number of times.
    Logs the results into a CSV file with columns for API requests, time spent, and iteration count.
    """
    csv_file_path = 'results/iteration_results_3_2.csv'
    fieldnames = ['Iteration', 'Total Time (seconds)', 'Compilation Success']

    # Initialize CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

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

        # Log results to CSV
        with open(csv_file_path, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({
                'Iteration': i + 1,
                'Total Time (seconds)': state['total_time'],
                'Compilation Success': compilation_success
            })

        print(f"Test Iteration{i} finished")
    	
        # Clear all files after each run
        clear_all_files()

    print(f"Completed {num_iterations} iterations. Results saved to {csv_file_path}.")

# reset everything to ensure working code
clear_all_files()
process_c_files(r"compile_project\src")
source_code_path = r'compile_project\src\main.c'

fixed_code = fix_c_code(source_code_path)

# Run the iteration process 100 times
run_iterations_without_interface(10)
