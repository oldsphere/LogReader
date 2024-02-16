from typing import List
import re

DictPattern = str

def read_content(filepath: str) -> str:
    with open(filepath, "r") as fid:
        content = fid.read()
    return content

def clip(clip_pattern: DictPattern, content:str) -> List[str]:
    for match in re.finditer(clip_pattern, content, re.MULTILINE):
        print(match)
    return [ "", "", "" ]

