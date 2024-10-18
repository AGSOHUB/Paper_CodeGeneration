import subprocess

# Path to MSYS2's mintty executable
mintty_path = r'C:\msys64\usr\bin\mintty.exe'

# Commands to execute
commands = '''
cd /
cd Paper_CodeGeneration/compile_project
./build.bat
'''

# Combine the commands into a single string
command_str = ' && '.join([cmd.strip() for cmd in commands.strip().split('\n')])

subprocess.Popen([
    mintty_path,
    '-i',  # Start as interactive shell
    'C:/msys64/Paper_CodeGeneration/agsotec_icon.ico', '/usr/bin/bash', '--login', '-i', '-c', command_str
])