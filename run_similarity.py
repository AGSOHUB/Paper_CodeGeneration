import json
import re
import difflib
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
import subprocess
import csv

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
    Reads a number from the given CSV file and deletes the file.
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

    # Delete the file
    os.remove(file_path)

    return number
load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

# Tokenization function to split code into tokens for similarity calculation
def tokenize(line):
    # Tokenize based on word boundaries and sequences of characters
    return re.findall(r'\b\w+\b', line)

# Similarity calculation between two pieces of code
def calculate_code_similarity(code1, code2):
    # Split the code into lines
    code1_lines = code1.splitlines()
    code2_lines = code2.splitlines()

    print(f"Comparing Code 1 with {len(code1_lines)} lines and Code 2 with {len(code2_lines)} lines")

    total_tokens = 0
    matching_tokens = 0

    # Convert lines to sets for exact match comparison
    code1_lines_set = set(code1_lines)
    code2_lines_set = set(code2_lines)
    
    exact_matches = code1_lines_set & code2_lines_set
    
    print(f"Found {len(exact_matches)} exact matching lines")

    # Count matching tokens from exact matches
    for line in exact_matches:
        tokens = tokenize(line)
        total_tokens += len(tokens)
        matching_tokens += len(tokens)
    
    # Remove exact matches from further comparison
    code1_lines = [line for line in code1_lines if line not in exact_matches]
    code2_lines = [line for line in code2_lines if line not in exact_matches]
    
    # Find approximate matches for remaining lines
    for line in code1_lines:
        tokens_line1 = tokenize(line)
        best_match = difflib.get_close_matches(line, code2_lines, n=1, cutoff=0.1)
        
        if best_match:
            tokens_line2 = tokenize(best_match[0])
            matcher = difflib.SequenceMatcher(None, tokens_line1, tokens_line2)
            matching_blocks = matcher.get_matching_blocks()

            for match in matching_blocks:
                matching_tokens += match.size

            total_tokens += max(len(tokens_line1), len(tokens_line2))
            code2_lines.remove(best_match[0])

    # Add remaining unmatched tokens
    for line in code1_lines + code2_lines:
        tokens = tokenize(line)
        total_tokens += len(tokens)

    similarity_percentage = (matching_tokens / total_tokens) * 100 if total_tokens > 0 else 0

    print(f"Similarity: {similarity_percentage:.2f}%")
    
    return similarity_percentage

# Function to read JSON file and calculate similarity across iterations
def calculate_similarity_over_iterations(test_version):
    file_path = f'results/{test_version}.json'
    
    # Check if file exists; if not, create an empty JSON structure
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump({test_version: []}, f)  # Initialize as an empty list or structure as needed
    
    # Read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f).get(test_version, [])

    similarities = []
    
    for i in range(1, len(data)):
        code1 = data[1]["Code"]
        code2 = data[i]["Code"]
        similarity = calculate_code_similarity(code1, code2)
        similarities.append(similarity)

    return similarities


def run_similarity(test_version):
    # Example usage: Replace 'test_data.json' with your actual JSON file path
    similarities = calculate_similarity_over_iterations(test_version)

    # Generate plot
    iterations = list(range(1, len(similarities) + 1))
    average_similarity = np.mean(similarities)

    plt.figure(figsize=(10, 6))
    plt.plot(iterations, similarities, marker='o', linestyle='-', color='b', label='Similarity')
    plt.axhline(y=average_similarity, color='r', linestyle='--', label=f'Average Similarity ({average_similarity:.2f}%)')
    plt.title('Code Similarity Across Iterations')
    plt.xlabel('Iteration')
    plt.ylabel('Similarity Percentage')
    plt.grid(True)
    plt.legend()

    # Save the plot to a file
    plt.savefig(f'code_similarity_plot{test_version}.png')

    # Display the plot
    plt.show()