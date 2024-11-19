import re
import os
from implementation.rag import generate_c_function, generate_c_variable, generate_c_typedef
from implementation.ast_find_missing import find_missing


def extract_includes(source_code):
    """
    Extracts the list of included header files from the C source code.
    """
    return re.findall(r'#include\s*[<"]([^>"]+)[>"]', source_code)

def read_file(file_path):
    """
    Reads the content of a file and returns it.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except (PermissionError, FileNotFoundError) as e:
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

def fix_c_code(file_path):
    """
    Detects missing functions, variables, and typedefs in a C source file and uses ChatGPT to generate and integrate them into the source code.
    """

    
    print("\n--- Phase 2: Code Generation ---")

    missing_functions, missing_variables, missing_typedefs = find_missing()
    if not missing_functions and not missing_variables and not missing_typedefs:
        print("nothing missing")

    print("Add missing functions:")

    # Generate and insert code for each unique missing function
    processed_functions = set()
    for index, (func_name, params) in enumerate(missing_functions):
        if func_name not in processed_functions:
            print(f"[{index + 1}/{len(missing_functions)}] {func_name} - Code generated")
            func_code = generate_c_function(func_name, params)
            file_path = r"compile_project\src\microcontroller_hal.h"
            insert_generated_code(func_code, file_path)
            processed_functions.add(func_name)

    print("Add missing variables:")

    # Generate and insert code for each unique missing variable
    processed_variables = set()
    for index, var_name in enumerate(missing_variables):
        if var_name not in processed_variables:
            print(f"[{index + 1}/{len(missing_variables)}] {var_name} - Code generated")

            var_code = generate_c_variable(var_name)
            file_path = r"compile_project\src\variables.h"
            insert_generated_code(var_code, file_path)
            processed_variables.add(var_name)

    # Generate and insert code for each unique missing typedef
    processed_typedefs = set()
    for index, typedef_name in enumerate(missing_typedefs):
        if typedef_name not in processed_typedefs:
            print(f"Generating code for typedef {index + 1}/{len(missing_typedefs)}: {typedef_name}")

            typedef_code = generate_c_typedef(typedef_name)
            file_path = r"compile_project\src\typedefs.h"
            insert_generated_code(typedef_code, file_path)
            processed_typedefs.add(typedef_name)

    return len(missing_functions) + len(missing_variables) + len(missing_typedefs)

def insert_generated_code(func_code, file_path):
    """
    Inserts the generated function code into the appropriate header file.
    """
    cleaned_code_lines = []
    inside_function = False
    inside_block_comment = False
    open_braces_count = 0

    # First loop: processes the lines to extract the function body and comments
    for line in func_code.splitlines():
        # Track if inside block comment
        if '/*' in line:
            inside_block_comment = True
        if '*/' in line:
            inside_block_comment = False
            cleaned_code_lines.append(line)
            continue

        # Detect the start of a function (e.g., 'void', other return types, or even indented function body)
        if 'void' in line or 'int' in line or 'return' in line or inside_function:
            # Once we detect a function or start writing inside a function, we track open/close braces
            if not inside_function:
                inside_function = True

            open_braces_count += line.count('{') - line.count('}')
            cleaned_code_lines.append(line)

            # End of the function when all open braces are closed
            if open_braces_count == 0 and inside_function:
                inside_function = False
            continue

        # Retain all comments (single-line or block comments)
        if inside_block_comment or line.strip().startswith('//'):
            cleaned_code_lines.append(line)

    # Second loop (bottom-up): remove lines after the first line that contains only a closing brace or parenthesis
    for i in range(len(cleaned_code_lines) - 1, -1, -1):
        line = cleaned_code_lines[i].strip()  # Strip any leading/trailing whitespace from the line
        if line == '}' or line == ')':
            # Once we find a line with only a closing brace or parenthesis, stop and remove everything after it
            cleaned_code_lines = cleaned_code_lines[:i+1]
            break

    cleaned_code = "\n".join(cleaned_code_lines).strip()


    # Append the cleaned code into the file
    with open(file_path, 'a') as file:
        file.write(f"\n{cleaned_code}\n")




def read_c_code(file_path):
    """
    Reads and returns the content and line count of a C code file.
    """
    with open(file_path, 'r') as file:
        code = file.read()
    return code, len(code.splitlines())
