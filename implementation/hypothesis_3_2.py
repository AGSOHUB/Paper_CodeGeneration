import re
import os
import time
import base64
from implementation.helper_functions.rag import process_c_files, generate_c_function, generate_c_variable, generate_c_typedef
from implementation.helper_functions.removed_unused_or_duplicated import find_and_remove_duplicates
from implementation.helper_functions.find_missing import find_missing


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


    missing_functions, missing_variables, missing_typedefs = find_missing()
    if not missing_functions and not missing_variables and not missing_typedefs:
        print("nothing missing")

    # Generate and insert code for each unique missing function
    processed_functions = set()
    for index, (func_name, params) in enumerate(missing_functions):
        if func_name not in processed_functions:
            print(f"Generating code for function {index + 1}/{len(missing_functions)}: {func_name}")
#            st.session_state.api_requests += 1
            func_code = generate_c_function(func_name, params)
            file_path = r"compile_project\src\microcontroller_hal.h"
            insert_generated_code(func_code, file_path)
            processed_functions.add(func_name)

    # Generate and insert code for each unique missing variable
    processed_variables = set()
    for index, var_name in enumerate(missing_variables):
        if var_name not in processed_variables:
            print(f"Generating code for variable {index + 1}/{len(missing_variables)}: {var_name}")
#            st.session_state.api_requests += 1
            var_code = generate_c_variable(var_name)
            file_path = r"compile_project\src\variables.h"
            insert_generated_code(var_code, file_path)
            processed_variables.add(var_name)

    # Generate and insert code for each unique missing typedef
    processed_typedefs = set()
    for index, typedef_name in enumerate(missing_typedefs):
        if typedef_name not in processed_typedefs:
            print(f"Generating code for typedef {index + 1}/{len(missing_typedefs)}: {typedef_name}")
#            st.session_state.api_requests += 1
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

# Define a CSS style for the code block
code_block_style = """
<style>
    .code-block {{
        font-family: Monaco, 'Courier New', monospace;
        background-color: #272822;
        color: #f8f8f2;
        padding: 10px;
        margin: 10px;
        border-radius: 5px;
        height: 200px;  /* Fixed height */
        overflow: auto; /* Enable scrolling */
        width: 100%;
        font-size: 16px;
        line-height: 1.5;
        white-space: pre-wrap;  /* Maintains whitespace formatting */
    }}

    .code-line-count {{
        font-size: 10px;
        color: #999;
    }}
</style>
"""

# Function to convert image file to base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    return f"data:image/jpg;base64,{encoded}"


def generation_cycle():
    if 'iteration' not in st.session_state:
        st.session_state.iteration = 0
        st.session_state.api_requests = 0
        st.session_state.total_time = 0.0

    # Button to start the generation cycle
    button1 = st.button("Generate")

    # Create placeholders for iteration count, API request count, and total time
    iteration_placeholder = st.empty()
    api_request_placeholder = st.empty()
    timer_placeholder = st.empty()

    if 'file_placeholders' not in st.session_state:
        st.session_state.file_placeholders = {
            "main.c": (st.empty(), st.empty(), st.empty()),
            "variables.h": (st.empty(), st.empty(), st.empty()),
            "microcontroller_hal.h": (st.empty(), st.empty(), st.empty()),
            "typedefs.h": (st.empty(), st.empty(), st.empty())
        }

    # Display the CSS style
    st.markdown(code_block_style, unsafe_allow_html=True)

    if button1 or st.session_state.iteration > 0:
        # Start the timer for the iteration
        start_time = time.time()
        while st.session_state.iteration < 15:
            process_c_files(r"compile_project\src")

            # Example usage
            source_code_path = r'compile_project\src\main.c'

            fixed_code = fix_c_code(source_code_path)

            st.session_state.iteration += 1
            print(f"######################Iteration {st.session_state.iteration}####################################")

            if not fixed_code:
                # Final update for the placeholders
                iteration_placeholder.markdown(f"**Iteration count: {st.session_state.iteration}**")
                api_request_placeholder.markdown(f"**API Requests: {st.session_state.api_requests}**")
                timer_placeholder.markdown(f"**Total Time: {st.session_state.total_time:.2f} seconds**")
                break


            # Calculate and update the elapsed time for the iteration
            elapsed_time = time.time() - start_time
            st.session_state.total_time += elapsed_time

            # Final update for the placeholders
            iteration_placeholder.markdown(f"**Iteration count: {st.session_state.iteration}**")
            api_request_placeholder.markdown(f"**API Requests: {st.session_state.api_requests}**")
            timer_placeholder.markdown(f"**Total Time: {st.session_state.total_time:.2f} seconds**")

            st.rerun()

        st.session_state.iteration = 0
    # Log display section
    log_data = display_logs()
    st.text_area("Log Output", log_data, height=300)
# generation_cycle()
