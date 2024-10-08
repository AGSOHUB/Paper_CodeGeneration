import streamlit as st
from implementation.hypothesis_3_2 import generation_cycle
from implementation.helper_functions.file_windows import show_file_windows, reload_content_general
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")



if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'code_generated' not in st.session_state:
    st.session_state.code_generated = ""



def concatenate_files(output_file):
    """Concatenate content from multiple files and write to the output file."""
    # Define the exact file paths
    file_paths = [
        'compile_project/src/typedefs.h',
        'compile_project/src/variables.h',
        'compile_project/src/microcontroller_hal.h'
    ]
    
    # Store the concatenated content
    concatenated_content = ''
    
    for file_path in file_paths:
        with open(file_path, 'r') as infile:
            content = infile.read()
            # Remove all instances of #include <stdint.h> and #include "variables.h"
            content = content.replace('#include <stdint.h>', '')
            content = content.replace('#include "variables.h"', '')
            concatenated_content += content
            concatenated_content += '\n'  # Ensure each file's content is separated by a newline

    with open(output_file, 'w') as outfile:
        # Add a single #include <stdint.h> at the top
        outfile.write('#include <stdint.h>\n\n')
        # Write the concatenated content
        outfile.write(concatenated_content)

    return output_file


def concatenate_file():
    """Concatenate content from multiple files and write to the output file."""
    # Define the exact file paths
    file_paths = [
        'compile_project/src/typedefs.h',
        'compile_project/src/variables.h',
        'compile_project/src/microcontroller_hal.h'
    ]
    
    # Store the concatenated content
    concatenated_content = ''
    
    for file_path in file_paths:
        with open(file_path, 'r') as infile:
            content = infile.read()
            # Remove all instances of #include <stdint.h> and #include "variables.h"
            content = content.replace('#include <stdint.h>', '')
            content = content.replace('#include "variables.h"', '')
            concatenated_content += content
            concatenated_content += '\n'  # Ensure each file's content is separated by a newline

    return concatenated_content

def overwrite_file(source_path, target_path):
    """Function to read content from the source path and overwrite the target file."""
    try:
        with open(source_path, 'r') as source_file:
            content = source_file.read()

        with open(target_path, 'w') as target_file:
            target_file.write(content)

        st.success(f"Content from {source_path} has been successfully overwritten to {target_path}.")
    except FileNotFoundError:
        st.error("Source file not found.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

    st.rerun()

def run_parallel_interface():
    if 'reload_done' not in st.session_state:
        st.session_state.reload_done = False
    if st.session_state.reload_done != True:
        reload_content_general()



    show_file_windows()

    generation_cycle()


#   output_file = 'microcontroller_hal.h'
#   concatenated_file = concatenate_files(output_file)
#   with open(concatenated_file, 'rb') as f:
#        st.download_button('Download microcontroller_hal.h', f, file_name=output_file)
    # Button to overwrite the Hardware Abstraction Layer file
    if st.button("Overwrite Hardware Abstraction Layer"):
        target_path = r"compile_project/src/microcontroller_hal.h"
        try:
            concatenate_files(target_path)
            st.success(f"The file {target_path} has been successfully overwritten with concatenated content.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    for message_html in reversed(st.session_state.conversation):
        st.markdown(message_html, unsafe_allow_html=True)



run_parallel_interface()