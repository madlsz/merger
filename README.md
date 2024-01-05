# merger.py

## Overview
This script is designed to be run on the root (main) file of a C or C++ project (`*.cpp` or `*.c`). It reads every file included in the project (only includes with paths relative to the root file, e.g., `#include "./some_header.hpp"`), creating a single file containing all of them. Note that the resulting file is not a valid C/C++ file and cannot be compiled.

## How it Works
The script works by parsing include statements in the main file and concatenating the content of each included file into a single output file.

## Why?
This script was created to automate the process of consolidating source code files, a requirement for submitting assignments at my college.

## Example
```
merger.py ./source.cpp ... ./result.cpp
```

## Usage
- The first argument (./source.cpp) is the path to the root file of your C/C++ project.
- You can provide as many root files as you want.
- The last argument (./result.cpp) is the desired output file.

## Potential Issues
- The resulting file is not a valid C/C++ file and cannot be compiled. Use it only for the specified purpose of consolidating source code files.

## License
This project is licensed under the terms of the MIT license. See the [LICENSE](./LICENSE) file for details.
