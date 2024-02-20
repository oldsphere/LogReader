from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer
from .content import read_content, clip, ClipContent

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
        run_content = self._split_runs(full_content)
        data = []
        for run in run_content:
            data.append(self._parse_run(run))
        return data

    def _parse_header(self, header:ClipContent) -> dict:
        return self.header_analyser.parse(header.content)

    def _parse_iteration(self, iteration:ClipContent) -> dict:
        return self.body_analyser.parse(iteration.content)

    def _parse_run(self, run_content: ClipContent) -> solverLogData:
        iterations = self._split_time(run_content.content)
        out = [self._parse_iteration(it.content) for it in iterations]
        return solverLogData(name="run")

    def _split_runs(self, content: str) -> List[ClipContent]:
        """Divide the multiple runs that a log file may containg due appendings"""
        return clip(clip_pattern=r"Build\s*:\s*(?P<build_number>.+)", content=content)

    def _split_time(self, content: str) -> List[ClipContent]:
        """Divide the run in the multiple timesteps iterations"""
        return clip(clip_pattern=r"\nTime\s*=\s*(?P<time>\d\.?\d*)", content=content)
