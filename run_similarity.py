import json
import re
import difflib
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv
import os
import subprocess
import csv
import openai
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)  # Replace with your actual API key

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


def get_embedding(text, model="text-embedding-3-small"):
    """
    Fetches the embedding for a given text using the specified model.
    Handles both string and dictionary inputs.
    """
    # If text is a dictionary, extract the "Code" key (or modify based on your JSON structure)
    if isinstance(text, dict):
        text = text.get("Code", "")
    
    # Ensure text is a string
    if not isinstance(text, str):
        raise ValueError(f"Invalid input for embedding. Expected string, got {type(text)}.")

    # Replace newlines to prevent errors
    text = text.replace("\n", " ")
    
    # Generate the embedding using the OpenAI client
    response = client.embeddings.create(input=[text], model=model)
    return response.data[0].embedding

# Function to calculate cosine similarity between two pieces of text
def calculate_embedding_similarity(code1, code2, model="text-embedding-3-small", iteration=None):
    """
    Calculates cosine similarity between embeddings of two code snippets.
    """
    # Get embeddings for the code snippets
    embedding1 = np.array(get_embedding(code1, model=model))
    embedding2 = np.array(get_embedding(code2, model=model))
    
    # Compute cosine similarity
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    
    # Print iteration and similarity in a single line
    if iteration is not None:
        print(f"Iteration {iteration}: Similarity = {similarity * 100:.2f}%")
    else:
        print(f"Similarity = {similarity * 100:.2f}%")
    
    return similarity * 100  # Convert to percentage

def calculate_similarity_over_iterations(data, model="text-embedding-3-small"):
    """
    Calculates similarity over multiple iterations from JSON data.
    """
    similarities = []

    for i in range(1, len(data)):
        code1 = data[0].get("Code")  # Extract "Code" key from first entry
        code2 = data[i].get("Code")  # Extract "Code" key from iteration
        
        # Ensure both code1 and code2 are valid strings
        if not isinstance(code1, str) or not isinstance(code2, str):
            print(f"Skipping iteration {i} due to invalid data format.")
            continue

        # Calculate similarity
        similarity = calculate_embedding_similarity(code1, code2, model=model)
        similarities.append(similarity)

    return similarities


def run_similarity_1(test_version = "test_data_3_2", iteration_ranges=[10, 30, 100]):

    file_path = f'results/{test_version}.json'
    
    # Read the JSON data
    with open(file_path, 'r') as f:
        data = json.load(f).get(test_version, [])

    if not data:
        print(f"No data found for test version: {test_version}")
        return

    # Calculate similarities
    similarities = calculate_similarity_over_iterations(data)

    # Prepare data for plotting
    means = []
    std_devs = []
    x_labels = []

    for max_iterations in iteration_ranges:
        # Limit data to the current range
        limited_similarities = similarities[:max_iterations]
        
        # Calculate mean and standard deviation
        mean_similarity = np.mean(limited_similarities)
        std_deviation = np.std(limited_similarities)
        
        # Store for plotting
        means.append(mean_similarity)
        std_devs.append(std_deviation)
        x_labels.append(f'{max_iterations} Iterations')

    # Create the plot with error bars
    plt.figure(figsize=(10, 6))
    plt.errorbar(x_labels, means, yerr=std_devs, fmt='o', capsize=5, linestyle='-', color='b', ecolor='r', label='Mean Similarity with Variance')
    
    # Annotate each point with the exact mean similarity
    for i, mean in enumerate(means):
        plt.text(i, mean, f'{mean:.2f}%', ha='center', va='bottom', fontsize=10, color='blue')

    plt.xlabel('Iteration Range')
    plt.ylabel('Similarity Percentage')
    plt.title('Average Code Similarity with Variance Across Iteration Ranges')
    plt.grid(True)
    plt.legend()

    # Save the plot as an SVG file
    plt.savefig(f'code_similarity_variance_{test_version}.svg', format='svg')

    # Display the plot
    plt.show()

run_similarity_1()