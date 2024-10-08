import os
import re

def read_file(file_path):
    """
    Reads the content of a file and returns it.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def write_file(file_path, content):
    """
    Writes content to a file.
    """
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing file {file_path}: {e}")

def find_definitions(source_code):
    """
    Finds all function, variable, and macro definitions in the source code.
    """
    functions = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(([^)]*)\)\s*\{', source_code)
    variables = re.findall(r'\b(?:[a-zA-Z_][a-zA-Z0-9_]*)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?:[=;])', source_code)
    macros = re.findall(r'#define\s+([a-zA-Z_][a-zA-Z0-9_]*)\s+', source_code)
    return set(functions), set(variables), set(macros)

def find_usages(source_code):
    """
    Finds all usages of functions, variables, and macros in the source code.
    """
    usages = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', source_code)
    return set(usages)

def remove_unused_code(file_path):
    """
    Removes unused functions, variables, and macros from the source code file.
    """
    source_code = read_file(file_path)
    if not source_code:
        return

    functions, variables, macros = find_definitions(source_code)
    usages = find_usages(source_code)

    unused_functions = {f[0] for f in functions if f[0] not in usages}
    unused_variables = {v for v in variables if v not in usages}
    unused_macros = {m for m in macros if m not in usages}

    # Remove unused functions
    for func in unused_functions:
        source_code = re.sub(rf'\b{func}\s*\([^)]*\)\s*\{{[^}}]*\}}', '', source_code, flags=re.DOTALL)

    # Remove unused variables
    for var in unused_variables:
        source_code = re.sub(rf'\b(?:[a-zA-Z_][a-zA-Z0-9_]*)\s+{var}\s*(?:[=;])[^;]*;', '', source_code)

    # Remove unused macros
    for macro in unused_macros:
        source_code = re.sub(rf'#define\s+{macro}\s+.*', '', source_code)

    write_file(file_path, source_code)
    print(f"Removed unused code from {file_path}")

def find_and_remove_duplicates(directories):
    """
    Finds and removes duplicate functions, variables, and macros across files in multiple directories.
    """
    all_functions = {}
    all_variables = {}
    all_macros = {}

    # Gather all definitions
    for directory in directories:
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(('.c', '.h')):
                    file_path = os.path.join(root, file)
                    source_code = read_file(file_path)
                    if not source_code:
                        continue

                    functions, variables, macros = find_definitions(source_code)
                    for func in functions:
                        if func[0] in all_functions:
                            all_functions[func[0]].append(file_path)
                        else:
                            all_functions[func[0]] = [file_path]
                    for var in variables:
                        if var in all_variables:
                            all_variables[var].append(file_path)
                        else:
                            all_variables[var] = [file_path]
                    for macro in macros:
                        if macro in all_macros:
                            all_macros[macro].append(file_path)
                        else:
                            all_macros[macro] = [file_path]

    # Remove duplicates
    for name, files in all_functions.items():
        if len(files) > 1:
            for file_path in files[1:]:
                remove_function_or_variable(file_path, name, is_function=True)
                print(f"Removed duplicate function {name} from {file_path}")

    for name, files in all_variables.items():
        if len(files) > 1:
            for file_path in files[1:]:
                remove_function_or_variable(file_path, name, is_function=False)
                print(f"Removed duplicate variable {name} from {file_path}")

    for name, files in all_macros.items():
        if len(files) > 1:
            for file_path in files[1:]:
                remove_macro(file_path, name)
                print(f"Removed duplicate macro {name} from {file_path}")

def remove_function_or_variable(file_path, name, is_function=True):
    """
    Removes a specific function or variable definition from the source code file.
    """
    source_code = read_file(file_path)
    if not source_code:
        return

    if is_function:
        source_code = re.sub(rf'\b{name}\s*\([^)]*\)\s*\{{[^}}]*\}}', '', source_code, flags=re.DOTALL)
    else:
        source_code = re.sub(rf'\b(?:[a-zA-Z_][a-zA-Z0-9_]*)\s+{name}\s*(?:[=;])[^;]*;', '', source_code)

    write_file(file_path, source_code)

def remove_macro(file_path, name):
    """
    Removes a specific macro definition from the source code file.
    """
    source_code = read_file(file_path)
    if not source_code:
        return

    source_code = re.sub(rf'#define\s+{name}\s+.*', '', source_code)
    write_file(file_path, source_code)
