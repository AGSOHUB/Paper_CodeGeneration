import subprocess
import os

# Path to the directory where the batch file is located
build_directory = r'C:\msys64\Paper_CodeGeneration\compile_project'

# Path to the batch file (build.bat)
build_bat = os.path.join(build_directory, 'build.bat')

# Change the current working directory to where the batch file is located
os.chdir(build_directory)

# Execute the batch file using subprocess
subprocess.Popen([build_bat], shell=True)
