# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.28

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = "C:/Program Files/CMake/bin/cmake.exe"

# The command to remove a file.
RM = "C:/Program Files/CMake/bin/cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:/Users/Nutzer/Paper_CodeGeneration/compile_project

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:/Users/Nutzer/Paper_CodeGeneration/compile_project/build

# Utility rule file for STM32F4Template.bin.

# Include any custom commands dependencies for this target.
include src/CMakeFiles/STM32F4Template.bin.dir/compiler_depend.make

# Include the progress variables for this target.
include src/CMakeFiles/STM32F4Template.bin.dir/progress.make

src/CMakeFiles/STM32F4Template.bin: src/STM32F4Template.elf
	cd C:/Users/Nutzer/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-objcopy.exe -Obinary STM32F4Template.elf STM32F4Template.bin

STM32F4Template.bin: src/CMakeFiles/STM32F4Template.bin
STM32F4Template.bin: src/CMakeFiles/STM32F4Template.bin.dir/build.make
.PHONY : STM32F4Template.bin

# Rule to build all files generated by this target.
src/CMakeFiles/STM32F4Template.bin.dir/build: STM32F4Template.bin
.PHONY : src/CMakeFiles/STM32F4Template.bin.dir/build

src/CMakeFiles/STM32F4Template.bin.dir/clean:
	cd C:/Users/Nutzer/Paper_CodeGeneration/compile_project/build/src && $(CMAKE_COMMAND) -P CMakeFiles/STM32F4Template.bin.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/STM32F4Template.bin.dir/clean

src/CMakeFiles/STM32F4Template.bin.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" C:/Users/Nutzer/Paper_CodeGeneration/compile_project C:/Users/Nutzer/Paper_CodeGeneration/compile_project/src C:/Users/Nutzer/Paper_CodeGeneration/compile_project/build C:/Users/Nutzer/Paper_CodeGeneration/compile_project/build/src C:/Users/Nutzer/Paper_CodeGeneration/compile_project/build/src/CMakeFiles/STM32F4Template.bin.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : src/CMakeFiles/STM32F4Template.bin.dir/depend

