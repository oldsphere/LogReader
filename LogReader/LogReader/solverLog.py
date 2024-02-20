from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer
from .content import read_content, clip

from typing import List
from dataclasses import dataclass, field


@dataclass
class solverLogData:
    name: str


class solverLog:
    def __init__(self):
        self.body_analyser = LogAnalyzer()
        self.header_analyser = LogAnalyzer()
        self.create_analyzers()

    def create_analyzers(self):
        pass

    def parse(self, filepath: str) -> List[solverLogData]:
        full_content = read_content(filepath)

        run_clips = clip(
            clip_pattern=r"Build\s: (?P<build_number>.+)", content=full_content
        )

        for clip_fragment in run_clips:
            time_content = clip(
                clip_pattern=r"\nTime\s=\s(?P<time>\d\.?\d*)", content=clip_fragment.content
            )

        return []
