import random
import re
import os
import time
import subprocess
import csv
import difflib
import matplotlib.pyplot as plt
from implementation.helper_functions.find_missing import get_all_elements_from_codebase
from implementation.test_functions import clear_all_files, compile_code, concatenate_files
from implementation.hypothesis_3_2 import fix_c_code
from implementation.helper_functions.rag import process_c_files
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")

def remove_element_and_comment(input_file_path, element_to_remove):
    # Read the content of the source code file into a list of lines
    with open(input_file_path, 'r') as file:
        lines = file.readlines()

    # Step 1: Determine if the element is a function or a variable/macro
    is_function = False
    start_line = None
    end_line = None

    # Check for function definition
    function_pattern = r'^\s*(?:void|int|uint32_t|uint16_t|uint8_t|const|static)?\s*\b{}\b\s*\('.format(re.escape(element_to_remove))
    for i, line in enumerate(lines):
        if re.search(function_pattern, line):
            is_function = True
            start_line = i
            # Now, find the end of the function by counting braces
            brace_count = 0
            for j in range(i, len(lines)):
                brace_count += lines[j].count('{')
                brace_count -= lines[j].count('}')
                if brace_count == 0 and '}' in lines[j]:
                    end_line = j
                    break
            break

    # If not a function, check for variable/macro
    if not is_function:
        variable_pattern = r'^\s*#define\s+\b{}\b'.format(re.escape(element_to_remove))
        for i, line in enumerate(lines):
            if re.search(variable_pattern, line):
                start_line = i
                end_line = i
                break

    # If neither a function nor a variable was found, return
    if start_line is None or end_line is None:
        # print(f"Element '{element_to_remove}' was not found in {input_file_path}")
        return False

    # Step 2: If it's a function, iterate upwards to find the comment block, if it exists
    if is_function:
        comment_start_line = start_line
        for k in range(start_line - 1, -1, -1):
            # Remove empty lines directly above the comment
            if lines[k].strip() == '':
                comment_start_line = k
            elif lines[k].strip().startswith('/**'):
                comment_start_line = k
                break
            # Stop if we hit a non-empty line that isn't a comment
            elif lines[k].strip() and not lines[k].strip().startswith('*') and not lines[k].strip().startswith('//'):
                break
        start_line = comment_start_line

    # Step 3: Remove the identified lines (comment + function or just variable/macro)
    del lines[start_line:end_line + 1]

    # Step 4: Remove trailing lines that contain only spaces or are empty
    while lines and lines[-1].isspace():
        lines.pop()

    # Step 5: Write the modified content back to the file
    with open(input_file_path, 'w') as file:
        file.writelines(lines)

    remove_empty_lines(input_file_path)

    element_type = "Function" if is_function else "Variable/Macro"
    print(f"{element_type} '{element_to_remove}' and its associated comment and empty lines above have been removed from {input_file_path}")
    return True

def remove_empty_lines(file_path):
    # Open the file in read mode
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip()]

    # Open the file in write mode
    with open(file_path, 'w') as file:
        file.writelines(non_empty_lines)

def remove_random_element(elements, input_file_path):
    combined_elements = []
    elements_to_filter_out = {
        'variables': [
            'LED_ROOM1_PIN', 'LED_ROOM2_PIN', 'WARN_LED_PIN', 
            'LED_PORT_BASE', 'TOUCH_SENSOR1_PIN', 'TOUCH_SENSOR2_PIN', 
            'MAGNET_SENSOR1_PIN', 'MAGNET_SENSOR2_PIN', 'LDR_PIN', 
            'SENSOR_PORT_BASE', 'touch_sensor1_state', 'touch_sensor2_state',
            'magnet_sensor1_state', 'magnet_sensor2_state', 'ldr_state'
        ],
        'functions': ['initialize_gpio_pins', 'main']
    }

    for key, value in elements.items():
        filtered_elements = [
            element for element in value if element not in elements_to_filter_out.get(key, [])
        ]
        combined_elements.extend([(key, element) for element in filtered_elements])

    while combined_elements:
        element_type, element_name = random.choice(combined_elements)
        print(f"Attempting to remove {element_type[:-1]}: {element_name}")
        
        # Attempt to remove the element from the file
        removal_successful = remove_element_and_comment(input_file_path, element_name)
        removal_successful_in_header = remove_element_and_comment(r'compile_project\src\variables.h', element_name)
        
        if removal_successful or removal_successful_in_header:
            return element_name

        # If removal was not successful, remove this element from the list to try the next one
        combined_elements.remove((element_type, element_name))

    print("No elements available to remove.")
    return None


def tokenize(line):
    # Tokenisierung anhand von Wortgrenzen und Zeichenfolgen
    return re.findall(r'\b\w+\b', line)

def calculate_code_similarity(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        file1_lines = f1.readlines()
        file2_lines = f2.readlines()

    total_tokens = 0
    matching_tokens = 0

    file1_lines_set = set(file1_lines)
    file2_lines_set = set(file2_lines)
    
    exact_matches = file1_lines_set & file2_lines_set
    
    for line in exact_matches:
        tokens = tokenize(line)
        total_tokens += len(tokens)
        matching_tokens += len(tokens)
    
    file1_lines = [line for line in file1_lines if line not in exact_matches]
    file2_lines = [line for line in file2_lines if line not in exact_matches]
    
    for line in file1_lines:
        tokens_line1 = tokenize(line)
        best_match = difflib.get_close_matches(line, file2_lines, n=1, cutoff=0.1)
        
        if best_match:
            tokens_line2 = tokenize(best_match[0])
            matcher = difflib.SequenceMatcher(None, tokens_line1, tokens_line2)
            matching_blocks = matcher.get_matching_blocks()

            for match in matching_blocks:
                matching_tokens += match.size

            total_tokens += max(len(tokens_line1), len(tokens_line2))
            file2_lines.remove(best_match[0])

    for line in file1_lines + file2_lines:
        tokens = tokenize(line)
        total_tokens += len(tokens)

    similarity_percentage = (matching_tokens / total_tokens) * 100 if total_tokens > 0 else 0

    return similarity_percentage

def save_plot(x, y, xlabel, ylabel, title, filename, plot_type="line"):
    plt.figure()
    if plot_type == "line":
        plt.plot(x, y, marker='o')
    elif plot_type == "bar":
        plt.bar(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.savefig(filename)
    plt.close()

def run_iterations_with_random_removal(num_iterations):
    os.makedirs('plots', exist_ok=True)
    csv_file_path = 'results/iteration_results_3_1.csv'
    fieldnames = ['Iteration', 'API Requests', 'Total Time (seconds)', 'Compilation Success', 'Similarity with Previous', 'Similarity with Original', 'Removed Element']

    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    previous_file_path = None
    original_concatenated_file_path = None

    iteration_numbers = []
    variances_with_previous = []
    variances_with_original = []
    api_requests = []
    total_times = []
    compilation_successes = []
    removed_elements = []

    for i in range(num_iterations):
        process_c_files(r"compile_project\src")
        state = {'iteration': i + 1, 'api_requests': 0, 'total_time': 0.0}


        
        elements = get_all_elements_from_codebase()

        source_code_path = r'compile_project\src\microcontroller_hal.h'
        removed_element = remove_random_element(elements, source_code_path)
        start_time = time.time()
        fixed_code = fix_c_code(source_code_path, [r'\compile_project\include'])
        elapsed_time = time.time() - start_time
        concatenated_file_path = f'output/concatenated_code_iteration_{i+1}.c'
        concatenate_files(concatenated_file_path)


        state['total_time'] = elapsed_time

        compilation_success = compile_code(r'compile_project\src\main.c')

        # If this is the first iteration, save the concatenated file path as the original reference
        if i == 0:
            original_concatenated_file_path = concatenated_file_path

        variance_with_previous = 0.0
        variance_with_original = 0.0
        if previous_file_path:
            variance_with_previous = calculate_code_similarity(previous_file_path, concatenated_file_path)
        variance_with_original = calculate_code_similarity(original_concatenated_file_path, concatenated_file_path)

        iteration_numbers.append(i + 1)
        variances_with_previous.append(variance_with_previous)
        variances_with_original.append(variance_with_original)
        api_requests.append(state['api_requests'])
        total_times.append(state['total_time'])
        compilation_successes.append(int(compilation_success))
        removed_elements.append(removed_element if removed_element else "None")

        with open(csv_file_path, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writerow({
                'Iteration': i + 1,
                'API Requests': state['api_requests'],
                'Total Time (seconds)': state['total_time'],
                'Compilation Success': compilation_success,
                'Similarity with Previous': variance_with_previous,
                'Similarity with Original': variance_with_original,
                'Removed Element': removed_element if removed_element else "None"
            })

        previous_file_path = concatenated_file_path



    print(f"Completed {num_iterations} iterations. Results saved to {csv_file_path}.")


# reset everything to ensure working code
clear_all_files()
process_c_files(r"compile_project\src")
source_code_path = r'compile_project\src\main.c'
include_directories = [r'\compile_project\include']

fixed_code = fix_c_code(source_code_path, include_directories)

# Run the iteration process with random element removal 100 times
run_iterations_with_random_removal(100)
