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

# Include any dependencies generated for this target.
include src/CMakeFiles/STM32F4Template.elf.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include src/CMakeFiles/STM32F4Template.elf.dir/compiler_depend.make

# Include the progress variables for this target.
include src/CMakeFiles/STM32F4Template.elf.dir/progress.make

# Include the compile flags for this target's objects.
include src/CMakeFiles/STM32F4Template.elf.dir/flags.make

src/CMakeFiles/STM32F4Template.elf.dir/main.c.obj: src/CMakeFiles/STM32F4Template.elf.dir/flags.make
src/CMakeFiles/STM32F4Template.elf.dir/main.c.obj: C:/msys64/Paper_CodeGeneration/compile_project/src/main.c
src/CMakeFiles/STM32F4Template.elf.dir/main.c.obj: src/CMakeFiles/STM32F4Template.elf.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=C:/msys64/Paper_CodeGeneration/compile_project/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object src/CMakeFiles/STM32F4Template.elf.dir/main.c.obj"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT src/CMakeFiles/STM32F4Template.elf.dir/main.c.obj -MF CMakeFiles/STM32F4Template.elf.dir/main.c.obj.d -o CMakeFiles/STM32F4Template.elf.dir/main.c.obj -c C:/msys64/Paper_CodeGeneration/compile_project/src/main.c

src/CMakeFiles/STM32F4Template.elf.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/STM32F4Template.elf.dir/main.c.i"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E C:/msys64/Paper_CodeGeneration/compile_project/src/main.c > CMakeFiles/STM32F4Template.elf.dir/main.c.i

src/CMakeFiles/STM32F4Template.elf.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/STM32F4Template.elf.dir/main.c.s"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S C:/msys64/Paper_CodeGeneration/compile_project/src/main.c -o CMakeFiles/STM32F4Template.elf.dir/main.c.s

src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj: src/CMakeFiles/STM32F4Template.elf.dir/flags.make
src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj: C:/msys64/Paper_CodeGeneration/compile_project/src/system_stm32f4xx.c
src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj: src/CMakeFiles/STM32F4Template.elf.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=C:/msys64/Paper_CodeGeneration/compile_project/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building C object src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -MD -MT src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj -MF CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj.d -o CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj -c C:/msys64/Paper_CodeGeneration/compile_project/src/system_stm32f4xx.c

src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing C source to CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.i"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E C:/msys64/Paper_CodeGeneration/compile_project/src/system_stm32f4xx.c > CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.i

src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling C source to assembly CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.s"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S C:/msys64/Paper_CodeGeneration/compile_project/src/system_stm32f4xx.c -o CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.s

src/CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.obj: src/CMakeFiles/STM32F4Template.elf.dir/flags.make
src/CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.obj: C:/msys64/Paper_CodeGeneration/compile_project/src/startup_stm32f40_41xxx.s
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --progress-dir=C:/msys64/Paper_CodeGeneration/compile_project/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building ASM object src/CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.obj"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(ASM_DEFINES) $(ASM_INCLUDES) $(ASM_FLAGS) -o CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.obj -c C:/msys64/Paper_CodeGeneration/compile_project/src/startup_stm32f40_41xxx.s

src/CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Preprocessing ASM source to CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.i"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(ASM_DEFINES) $(ASM_INCLUDES) $(ASM_FLAGS) -E C:/msys64/Paper_CodeGeneration/compile_project/src/startup_stm32f40_41xxx.s > CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.i

src/CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green "Compiling ASM source to assembly CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.s"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe $(ASM_DEFINES) $(ASM_INCLUDES) $(ASM_FLAGS) -S C:/msys64/Paper_CodeGeneration/compile_project/src/startup_stm32f40_41xxx.s -o CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.s

# Object files for target STM32F4Template.elf
STM32F4Template_elf_OBJECTS = \
"CMakeFiles/STM32F4Template.elf.dir/main.c.obj" \
"CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj" \
"CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.obj"

# External object files for target STM32F4Template.elf
STM32F4Template_elf_EXTERNAL_OBJECTS =

src/STM32F4Template.elf: src/CMakeFiles/STM32F4Template.elf.dir/main.c.obj
src/STM32F4Template.elf: src/CMakeFiles/STM32F4Template.elf.dir/system_stm32f4xx.c.obj
src/STM32F4Template.elf: src/CMakeFiles/STM32F4Template.elf.dir/startup_stm32f40_41xxx.s.obj
src/STM32F4Template.elf: src/CMakeFiles/STM32F4Template.elf.dir/build.make
src/STM32F4Template.elf: lib/STM32F4xx_StdPeriph_Driver/libstm32f4xx.a
	@$(CMAKE_COMMAND) -E cmake_echo_color "--switch=$(COLOR)" --green --bold --progress-dir=C:/msys64/Paper_CodeGeneration/compile_project/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Linking C executable STM32F4Template.elf"
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && C:/msys64/mingw64/bin/arm-none-eabi-gcc.exe -mthumb -mcpu=cortex-m4 -mlittle-endian -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb-interwork --specs=nano.specs --specs=nosys.specs  -fno-builtin -Wall -std=gnu99 -fdata-sections -ffunction-sections -g3 -gdwarf-2 $(STM32F4Template_elf_OBJECTS) $(STM32F4Template_elf_EXTERNAL_OBJECTS) -o STM32F4Template.elf  ../lib/STM32F4xx_StdPeriph_Driver/libstm32f4xx.a -Wl,-Map=STM32F4Template.map,--cref,--no-warn-mismatch -g -Wl,--gc-sections -TC:/msys64/Paper_CodeGeneration/compile_project/linker/stm32f407vgt.ld

# Rule to build all files generated by this target.
src/CMakeFiles/STM32F4Template.elf.dir/build: src/STM32F4Template.elf
.PHONY : src/CMakeFiles/STM32F4Template.elf.dir/build

src/CMakeFiles/STM32F4Template.elf.dir/clean:
	cd C:/msys64/Paper_CodeGeneration/compile_project/build/src && $(CMAKE_COMMAND) -P CMakeFiles/STM32F4Template.elf.dir/cmake_clean.cmake
.PHONY : src/CMakeFiles/STM32F4Template.elf.dir/clean

src/CMakeFiles/STM32F4Template.elf.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" C:/msys64/Paper_CodeGeneration/compile_project C:/msys64/Paper_CodeGeneration/compile_project/src C:/msys64/Paper_CodeGeneration/compile_project/build C:/msys64/Paper_CodeGeneration/compile_project/build/src C:/msys64/Paper_CodeGeneration/compile_project/build/src/CMakeFiles/STM32F4Template.elf.dir/DependInfo.cmake "--color=$(COLOR)"
.PHONY : src/CMakeFiles/STM32F4Template.elf.dir/depend

