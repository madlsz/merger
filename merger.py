#!/usr/bin/env python

import sys
from pathlib import Path


class Dependency:
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        return self.path.name
    
    def __str__(self):
        return f"{self.path}"


def check_file(path, dependencies, cwd = Path.cwd()):
    new_dependency_found = False
    with open(path) as f:
        include_lines = [line.split()[1].replace('"','') for line in f.read().splitlines() if line.startswith("#include") and '"' in line]

    for line in include_lines:
        dependency = Dependency((cwd / Path(line)).resolve(strict=False))
        if dependency.name not in [d.name for d in dependencies]:
            dependencies.append(dependency)
            new_dependency_found = True
    if new_dependency_found:
        for dep in dependencies:
            check_file(dep.path, dependencies, dep.path.parent)


def main():
    if len(sys.argv) < 3:
        raise Exception(f"usage: {sys.argv[0]} src_file out_file")
    src_path = sys.argv[1]
    out_path = sys.argv[2]

    dependencies = [Dependency((Path.cwd() / Path(src_path)).resolve(strict=False))]

    check_file(src_path, dependencies)

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
    with open(out_path, "w", encoding="utf8") as f:
        f.write(out_file_content)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e) 
        input("press Enter to exit...")
