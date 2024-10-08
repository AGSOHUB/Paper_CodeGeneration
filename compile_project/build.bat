mkdir build
cd build && cmake -G "Unix Makefiles" -D "CMAKE_TOOLCHAIN_FILE=../CMake/GNU-ARM-Toolchain.cmake" ../
cmake . > cmake_log.txt 2>&1
make > build_log.txt 2>&1