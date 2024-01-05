#!/usr/bin/env python

import sys
import os
from pathlib import Path


class Dependency:
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return self.path.name
    
    def __str__(self):
        return f"{self.path}"


def check_file(path, dependencies, cwd):
    new_dependency_found = False
    with open(path) as f:
        include_lines = [line.split()[1].replace('"','') for line in f.read().splitlines() if line.startswith("#include") and '"' in line]

    for line in include_lines:
        dependency = Dependency((cwd / Path(line)).resolve(strict=False))
        if dependency.name not in [d.name for d in dependencies]:
            dependencies.append(dependency)
            check_file(dependency.path, dependencies, dependency.path.parent)


def main():
    if len(sys.argv) < 3:
        raise Exception(f"usage: {sys.argv[0]} src_file ... out_file")
    src_path = sys.argv[1:-1]
    out_path = sys.argv[-1]

    dependencies = []
    for path in src_path:
        dependency = Dependency((Path.cwd() / Path(path)).resolve(strict=False))
        if dependency.name not in [d.name for d in dependencies]:
            dependencies.append(Dependency((Path.cwd() / Path(path)).resolve(strict=False)))
            check_file(path, dependencies, dependency.path.parent)

    # prepare the out file content
    out_file_content = ""
    out_file_content += "// \n"
    out_file_content += "// \n"
    out_file_content += "// \n\n"
    for dependency in dependencies:
        out_file_content += f"// @@@@@@@@@@@@@@@@@@@@@@@@@@@\n// {dependency.name}\n// @@@@@@@@@@@@@@@@@@@@@@@@@@@\n"
        with open(dependency.path, encoding="utf8") as d:
            for line in d.read().splitlines():
                out_file_content += line + "\n"
        out_file_content += "\n"

    # write the out file content to the file
    choice = "y"
    if os.path.isfile(out_path):
        print(f"{out_path} exists and will be overwritten!")
        choice = input("Do you want to continue?[y/n]> ")
    if choice.lower() == "y":
        with open(out_path, "w", encoding="utf8") as f:
            f.write(out_file_content)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e) 
        input("press Enter to exit...")