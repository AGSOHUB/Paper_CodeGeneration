
from implementation.hypothesis_3_2 import generation_cycle
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

api_key = os.getenv("OPENAI_API_KEY")





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

