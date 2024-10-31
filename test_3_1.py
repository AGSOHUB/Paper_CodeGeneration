import random
import re
import os
import time
import json
import uuid
from datetime import datetime
import difflib
import matplotlib.pyplot as plt
from implementation.helper_functions.find_missing import get_all_elements_from_codebase
from implementation.test_functions import clear_all_files, compile_code, concatenate_files
from implementation.hypothesis_3_2 import fix_c_code
from implementation.helper_functions.rag import process_c_files
from dotenv import load_dotenv
import os
from interface_3 import concatenate_file
from run_similarity import run_similarity, run_build_bat, run_renode_script, read_and_delete_csv

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

def calculate_code_similarity(code1, code2):
    # Tokenize and calculate similarity between two strings of code
    code1_lines = code1.splitlines()
    code2_lines = code2.splitlines()

    total_tokens = 0
    matching_tokens = 0

    code1_lines_set = set(code1_lines)
    code2_lines_set = set(code2_lines)
    
    exact_matches = code1_lines_set & code2_lines_set
    
    for line in exact_matches:
        tokens = tokenize(line)
        total_tokens += len(tokens)
        matching_tokens += len(tokens)
    
    code1_lines = [line for line in code1_lines if line not in exact_matches]
    code2_lines = [line for line in code2_lines if line not in exact_matches]
    
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

    for line in code1_lines + code2_lines:
        tokens = tokenize(line)
        total_tokens += len(tokens)

    similarity_percentage = (matching_tokens / total_tokens) * 100 if total_tokens > 0 else 0

    return similarity_percentage

def run_iterations_with_random_removal(num_iterations):
    """
    Runs the iteration process with random element removal and logs the results in JSON format.
    """
    json_file_path = 'results/test_data_3_1.json'
    csv_file_path = 'results/simulation_test.csv'

    # Load or initialize the JSON data structure
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as json_file:
            test_data = json.load(json_file)
    else:
        test_data = {"test_data_3_1": []}

    for i in range(num_iterations):
        process_c_files(r"compile_project\src")
        state = {'iteration': i + 1, 'api_requests': 0, 'total_time': 0.0}

        elements = get_all_elements_from_codebase()
        source_code_path = r'compile_project\src\microcontroller_hal.h'
        removed_element = remove_random_element(elements, source_code_path)

        start_time = time.time()
        fix_c_code(source_code_path)
        elapsed_time = time.time() - start_time
        state['total_time'] = elapsed_time
        compilation_success = compile_code(r'compile_project\src\main.c')

        # Retrieve previous and original "Code" for similarity calculation
        previous_code = test_data["test_data_3_1"][-1]["Code"] if test_data["test_data_3_1"] else ""
        original_code = test_data["test_data_3_1"][0]["Code"] if test_data["test_data_3_1"] else ""

        current_code = concatenate_file()
        variance_with_previous = calculate_code_similarity(previous_code, current_code) if previous_code else 0.0
        variance_with_original = calculate_code_similarity(original_code, current_code) if original_code else 0.0

        # Run the build.bat file and Renode simulation
        run_build_bat()
        run_renode_script()

        # Read the Functioning code binary from the CSV and clear the file
        functioning_code_binary = read_and_delete_csv(csv_file_path)

        # Prepare the new entry
        new_entry = {
            "unique_id": str(uuid.uuid4()),
            "timestamp": datetime.now().isoformat(),
            "total time (seconds)": state['total_time'],
            "compilation-success": compilation_success,
            "Similarity with Previous": variance_with_previous,
            "Similarity with Original": variance_with_original,
            "Removed Element": removed_element if removed_element else "None",
            "Functioning code Binary": functioning_code_binary,
            "Code": current_code,
        }

        # Append the new entry to the test data
        test_data["test_data_3_1"].append(new_entry)

        # Save the updated JSON data
        with open(json_file_path, 'w') as json_file:
            json.dump(test_data, json_file, indent=4)

        print(f"Test Iteration {i + 1} finished. Results saved to {json_file_path}.")

    print(f"Completed {num_iterations} iterations.")


# reset everything to ensure working code
clear_all_files()
process_c_files(r"compile_project\src")
source_code_path = r'compile_project\src\main.c'
include_directories = [r'\compile_project\include']

fixed_code = fix_c_code(source_code_path)

# Run the iteration process with random element removal 100 times
run_iterations_with_random_removal(1)


run_similarity('test_data_3_1')
