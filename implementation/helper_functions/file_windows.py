import streamlit as st
import os
import json
import shutil

def reload_content_general():
    # List of file paths
    file_paths = [
        "compile_project/src/variables.h",
        "compile_project/src/microcontroller_hal.h",
        "compile_project/src/typedefs.h"

    ]

    # Corresponding initial content for each file
    initial_code = [
        "//variables \n#include <stdint.h>",
        '//microcontroller_h.h \n#include <stdint.h> \n#include "variables.h"',
        "//typedefs.h \n#include <stdint.h>"
    ]

    # Clearing the contents of each file and writing initial content
    for file_path, code in zip(file_paths, initial_code):
        with open(file_path, "w") as f:
            f.write(code)
    
#    source_path = r"compile_project/src/main.c"
#    target_path = "compile_project/src/main.c"
#    reload_file(source_path, target_path)


#   source_path = r"compile_project/src/microcontroller_hal.h"
#   target_path = "compile_project/src/microcontroller_hal.h"
#   reload_file(source_path, target_path)

    # TODO: Add new content to a file while preserving existing content
    target_file = "compile_project/src/microcontroller_hal.h"  # Replace with the actual file you want to update
    new_content = '//microcontroller_h.h \n#include <stdint.h> \n#include "variables.h"\n'

    # Read existing content
    with open(target_file, "r") as f:
        existing_content = f.read()

    # Write new content followed by existing content
    with open(target_file, "w") as f:
        f.write(new_content + existing_content)

    st.session_state.reload_done = True


def reload_file(source_path, target_path):
    try:
        # Extracting file names from paths
        source_file_name = os.path.basename(source_path)

        # Reading content from the source file
        with open(source_path, 'r') as source_file:
            content = source_file.read()

        # Writing content to the target file
        with open(target_path, 'w') as target_file:
            target_file.write(content)

        # Displaying success message with file names
        st.success(f"Content reloaded from {source_file_name}")
    except FileNotFoundError:
        st.error("Source file not found.")

# Function to read the code and count lines
def read_c_code(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code, len(code.splitlines())



def show_file_windows():
    # st.title('Streamlit JSON Data App')

    # Define the common style for the code blocks
    code_block_style = f"""
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
</style>"""


    # Read the code from the files
    code_generation_constants, lines_constants = read_c_code("compile_project/src/main.c")
    code_generation_voids, lines_voids = read_c_code("compile_project/src/variables.h")
    code_generation_voids_main, lines_voids_main = read_c_code("compile_project/src/microcontroller_hal.h")

    # Display the CSS style
    st.markdown(code_block_style, unsafe_allow_html=True)

    # Display the code blocks with file names and line counts
    st.markdown("### compile_project/src/main.c")
    st.markdown(f"<div class='code-block'><pre>{code_generation_constants}</pre></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='code-line-count'>{lines_constants} lines</div>", unsafe_allow_html=True)
    st.markdown("\n")
    st.markdown("### compile_project/src/variables.h")
    st.markdown(f"<div class='code-block'><pre>{code_generation_voids}</pre></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='code-line-count'>{lines_voids} lines</div>", unsafe_allow_html=True)
    st.markdown("\n")
    st.markdown("### compile_project/src/microcontroller_hal.h")
    st.markdown(f"<div class='code-block'><pre>{code_generation_voids_main}</pre></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='code-line-count'>{lines_voids_main} lines</div>", unsafe_allow_html=True)
    st.markdown("\n")  
    with st.sidebar:
        # Button to reload the application file
        if st.button("Reload Application-File"):
            source_path = r"compile_project/src/main.c"
            target_path = "compile_project/src/main.c"
            reload_file(source_path, target_path)
            st.rerun()

        if st.button("Clear All Files"):
            open('output/generation_log.txt', 'w').close()
            # List of file paths
            file_paths = [
                "compile_project/src/variables.h",
                "compile_project/src/microcontroller_hal.h",
                "compile_project/src/typedefs.h",
                "compile_project/src/main.i",
                "compile_project/src/variables.h",

            ]

            # Corresponding initial content for each file
            initial_code = [
                "//variables \n#include <stdint.h>",
                '//microcontroller_h.h \n#include <stdint.h> \n#include "variables.h"',
                "//typedefs.h \n#include <stdint.h>",
                "","#include <stdint.h>"
            ]

            # Clearing the contents of each file and writing initial content
            for file_path, code in zip(file_paths, initial_code):
                with open(file_path, "w") as f:
                    f.write(code)

            # Deleting all files in the vector_stores folder
            folder_path = "vector_stores"
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                st.success("All files in the 'vector_stores' folder have been deleted.")
            else:
                st.warning(f"The folder '{folder_path}' does not exist.")

            st.success("All files have been reset to initial state.")
            st.rerun()

        
        st.markdown(
            """
                ### Application layer:
                -> The 1. Window
\n\n
                ### Lower Level Layer
                -> 2. Window for generated variables\n
                -> 3. Window for generated functions
                    
            """)