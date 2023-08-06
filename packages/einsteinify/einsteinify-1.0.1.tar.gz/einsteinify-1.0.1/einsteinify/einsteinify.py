import os
import re
from pathlib import Path

def einsteinify_line(path: Path, line: str) -> str:
    to_replace = '.'
    while (str(path) != '.'):
        if str(path) in line:
            return line.replace(str(path), to_replace, 1)
        path = path.parent
        to_replace += '.'
    return line


def einsteinify(path: str) -> None:
    root_path = Path(path).parent
    for root, _, files in os.walk(path):
        base_path = Path(root).relative_to(root_path)
        for file in files:
            file_path = Path(root).joinpath(file)
            parsed_lines = []
            with file_path.open(mode='r') as input:
                for line in input:
                    matches = re.findall(r'#include "(.+)"', line)
                    parsed_line = line if not matches else einsteinify_line(Path(base_path), line)
                    parsed_lines.append(parsed_line)
            new_text = ''.join(parsed_lines)
            file_path.write_text(new_text)