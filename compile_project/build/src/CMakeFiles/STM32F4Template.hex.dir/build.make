# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.30

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
CMAKE_COMMAND = C:/Users/SebastianHaug/mingw64/bin/cmake.exe

# The command to remove a file.
RM = C:/Users/SebastianHaug/mingw64/bin/cmake.exe -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:/msys64/Paper_CodeGeneration/compile_project

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:/msys64/Paper_CodeGeneration/compile_project/build

# Utility rule file for STM32F4Template.hex.

# Include any custom commands dependencies for this target.
include src/CMakeFiles/STM32F4Template.hex.dir/compiler_depend.make

# Include the progress variables for this target.
include src/CMakeFiles/STM32F4Template.hex.dir/progress.make

src/CMakeFiles/STM32F4Template.hex: src/STM32F4Template.elf
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-objcopy.exe -Oihex STM32F4Template.elf STM32F4Template.hex

STM32F4Template.hex: src/CMakeFiles/STM32F4Template.hex
STM32F4Template.hex: src/CMakeFiles/STM32F4Template.hex.dir/build.make
.PHONY : STM32F4Template.hex

# Rule to build all files generated by this target.
src/CMakeFiles/STM32F4Template.hex.dir/build: STM32F4Template.hex
.PHONY : src/CMakeFiles/STM32F4Template.hex.dir/build

src/CMakeFiles/STM32F4Template.hex.dir/clean:
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && $(CMAKE_COMMAND) -P CMakeFiles/STM32F4Template.hex.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/STM32F4Template.hex.dir/clean

src/CMakeFiles/STM32F4Template.hex.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" C:/msys64/Paper_CodeGeneration/compile_project C:/msys64/Paper_CodeGeneration/compile_project/src C:/msys64/Paper_CodeGeneration/compile_project/build C:/msys64/Paper_CodeGeneration/compile_project/build/src C:/msys64/Paper_CodeGeneration/compile_project/build/src/CMakeFiles/STM32F4Template.hex.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : src/CMakeFiles/STM32F4Template.hex.dir/depend

