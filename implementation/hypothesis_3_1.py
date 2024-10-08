import openai
import re
import os
from implementation.helper_functions.rag import process_c_files, generate_c_function


def extract_includes(source_code):
    """
    Extracts the list of included header files from the C source code.
    """
    includes = re.findall(r'#include\s*[<"]([^>"]+)[>"]', source_code)
    return includes

def analyze_c_code(source_code):
    """
    Analyzes the C source code for errors, specifically missing function definitions.
    Returns a list of missing function names.
    """
    defined_functions = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*\{', source_code)
    called_functions = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*;', source_code)
    missing_functions = [func for func in called_functions if func not in defined_functions]
    return list(set(missing_functions))

def read_file(file_path):
    """
    Reads the content of a file and returns it.
    """
    try:
        with open(file_path, 'r') as file:
            print(f"Reading file: {file_path}")
            return file.read()
    except PermissionError:
        print(f"Permission Denied: Unable to read file {file_path}")
        return None
    except FileNotFoundError:
        print(f"File Not Found: {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def scan_directory_for_headers(directory):
    """
    Scans a directory recursively for header files and returns their paths.
    """
    header_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.h'):
                header_files.append(os.path.join(root, file))
    return header_files

def scan_for_missing_functions(source_code, header_files):
    """
    Scans the source code and included header files for missing function definitions.
    """
    missing_functions = analyze_c_code(source_code)
    
    for header_file in header_files:
        header_code = read_file(header_file)
        if header_code:
            defined_functions = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*?\)\s*;', header_code)
            missing_functions = [func for func in missing_functions if func not in defined_functions]

    return missing_functions

def fix_c_code(file_path, include_directories):
    """
    Detects missing functions in a C source file and uses ChatGPT to generate and integrate them into the source code.
    """
    source_code = read_file(file_path)
    if not source_code:
        return None

    include_files = extract_includes(source_code)

    header_files = []
    for include_file in include_files:
        for directory in include_directories:
            potential_path = os.path.join(directory, include_file)
            if os.path.isfile(potential_path):
                header_files.append(potential_path)
                break

    header_files.extend(scan_directory_for_headers('.'))

    missing_functions = scan_for_missing_functions(source_code, header_files)
    fixed_code = source_code
    for func in missing_functions:
        func_code = generate_c_function(func)
        insert_generated_code(func_code)

def insert_generated_code(func_code):
    # Remove ``` and ```c from the function code
    cleaned_code = re.sub(r'```c?', '', func_code)
    
    file_path = r"compile_project\src\microcontroller_hal.h"
    
    # Append the cleaned code to the end of the file
    with open(file_path, 'a') as file:
        file.write(f"\n{cleaned_code}\n")
        

# Example usage
source_code_path = r'compile_project\src\main.c'
include_directories = [r'\compile_project\include']

# Update Vectorstore for Hardware Abstraction Layer
process_c_files("input")

fixed_code = fix_c_code(source_code_path, include_directories)

#if fixed_code:
#    print("Fixed Code:")
print(fixed_code)
#else:
#    print("Failed to fix code due to permission issues or file not found.")


