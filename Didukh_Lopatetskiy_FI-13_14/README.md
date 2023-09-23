# Long-Arithmetic-Lib

## Build and Usage

Follow these steps to build and run LongArithmeticLib, including tests and examples:

1. Clone the LongArithmeticLib repository to your local machine:
```bash
git clone <https://github.com/prumat4/Long-Arithmetic.git>
```

2. Navigate to the project directory:
```bash 
cd LongArithmeticLib
```

3. Create a build directory:
```bash
mkdir build
cd build
```
   
4. Generate the build system using CMake:
```bash
cmake ..
```

5. Build the library:
```bash
cmake --build .
```
   
Run Tests

1. After building the library, you can run the tests using the following command:
```bash
./test/LongArithmeticLibTests
```
   
Run Example Program

1. Once the library is built, you can run the example program by executing:
```bash
./example/main
```
   This program demonstrates the usage of LongArithmeticLib for long arithmetic operations.

Usage

To use LongArithmeticLib in your own project, follow these steps:

1. Include the necessary header files in your C++ code:
```c++
#include "LongArithmeticLib/LongArithmeti.hpp"
```

2. Link your project with the LongArithmeticLib library:
```cmake
target_link_libraries(YourProjectName LongArithmeticLib)
```

3. Use the provided functions for long arithmetic operations in your code.
