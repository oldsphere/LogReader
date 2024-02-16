from typing import List
from dataclasses import dataclass, field
import re

DictPattern = str

@dataclass
class ClipContent:
    name: str
    content: str = field(repr=False, init=False)
    start: int = 0
    end: int = 0

def read_content(filepath: str) -> str:
    with open(filepath, "r") as fid:
        content = fid.read()
    return content


def clip(clip_pattern: DictPattern, content: str) -> List[ClipContent]:
    clips = []
    for match in re.finditer(clip_pattern, content, re.MULTILINE):
        new_clip_name = match.group(1)
        last_clip_end, new_clip_begin = match.span()
        new_clip = ClipContent(name=new_clip_name, start=new_clip_begin) 
        clips.append(new_clip)
        if len(clips) < 2:
            continue
        last_clip = clips[-2]
        last_clip.end = last_clip_end-1
        last_clip.content = content[last_clip.start:last_clip.end]
    return clips
