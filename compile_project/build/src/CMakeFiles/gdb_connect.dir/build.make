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
CMAKE_COMMAND = C:/msys64/mingw64/bin/cmake.exe

# The command to remove a file.
RM = C:/msys64/mingw64/bin/cmake.exe -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = C:/msys64/Paper_CodeGeneration/compile_project

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = C:/msys64/Paper_CodeGeneration/compile_project/build

# Utility rule file for gdb_connect.

# Include any custom commands dependencies for this target.
include src/CMakeFiles/gdb_connect.dir/compiler_depend.make

# Include the progress variables for this target.
include src/CMakeFiles/gdb_connect.dir/progress.make

src/CMakeFiles/gdb_connect: src/STM32F4Template.elf
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && ARM_GDB_EXECUTABLE-NOTFOUND -ex "target remote localhost:4242" -ex "monitor reset halt" STM32F4Template.elf

gdb_connect: src/CMakeFiles/gdb_connect
gdb_connect: src/CMakeFiles/gdb_connect.dir/build.make
.PHONY : gdb_connect

# Rule to build all files generated by this target.
src/CMakeFiles/gdb_connect.dir/build: gdb_connect
.PHONY : src/CMakeFiles/gdb_connect.dir/build

src/CMakeFiles/gdb_connect.dir/clean:
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && $(CMAKE_COMMAND) -P CMakeFiles/gdb_connect.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/gdb_connect.dir/clean

src/CMakeFiles/gdb_connect.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" C:/msys64/Paper_CodeGeneration/compile_project C:/msys64/Paper_CodeGeneration/compile_project/src C:/msys64/Paper_CodeGeneration/compile_project/build C:/msys64/Paper_CodeGeneration/compile_project/build/src C:/msys64/Paper_CodeGeneration/compile_project/build/src/CMakeFiles/gdb_connect.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : src/CMakeFiles/gdb_connect.dir/depend
