from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer
from .content import read_content, clip, ClipContent

from typing import List, Dict
from dataclasses import dataclass, field


@dataclass
class TimeSerie:
    time: List[float] = field(default_factory=list)
    value: List[float] = field(default_factory=list)


@dataclass
class solverLogData:
    name: str

    @classmethod
    def extract_time_series(cls, out: List[dict]) -> Dict[str, TimeSerie]:

        def extract_single_time(globalDict: dict, timeDict: dict) -> None:
            time = timeDict.pop("time")
            for name, value in timeDict.items():
                if not globalDict.get(name):
                    globalDict[name] = TimeSerie()
                globalDict[name].time.append(time)
                globalDict[name].value.append(value)

        timeSeries = {}
        [extract_single_time(timeSeries, time_match) for time_match in out]
        return timeSeries

    def add_time_series(self, out: List[dict]) -> None:
        self.__dict__.update(self.extract_time_series(out))


class solverLog:
    def __init__(self):
        self.body_analyser = LogAnalyzer()
        self.header_analyser = LogAnalyzer()
        self.create_analyzers()

    def create_analyzers(self):
        # Header Analyzers
        self._analyzer_date_and_hour()
        self._analyzer_number_processors()
        # Body Analyzers
        self._analyzer_execution_time()

    def parse(self, filepath: str) -> List[solverLogData]:
        full_content = read_content(filepath)
        run_content = self._split_runs(full_content)
        data = []
        for run in run_content[1:]:
            data.append(self._parse_run(run))
        return data

    def _parse_header(self, header: ClipContent) -> dict:
        return self.header_analyser.parse(header.content)

    def _parse_iteration(self, iteration: ClipContent) -> dict:
        out = self.body_analyser.parse(iteration.content)
        out["time"] = float(iteration.name)
        return out

    def _parse_run(self, run_content: ClipContent) -> solverLogData:
        iterations = self._split_time(run_content.content)

        results = solverLogData(name="run")

        headerOut = self._parse_header(iterations.pop(0))
        print(headerOut)

        out = [self._parse_iteration(it) for it in iterations]
        results.add_time_series(out)
        return results

    def _split_runs(self, content: str) -> List[ClipContent]:
        """Divide the multiple runs that a log file may containg due appendings"""
        return clip(clip_pattern=r"Build\s*:\s*(?P<build_number>.+)", content=content)

    def _split_time(self, content: str) -> List[ClipContent]:
        """Divide the run in the multiple timesteps iterations"""
        return clip(clip_pattern=r"\nTime\s*=\s*(?P<time>\d\.?\d*)", content=content)

    def _analyzer_execution_time(self):
        self.body_analyser.add_numeric_regex(
            pattern=(
                r"ExecutionTime = (?P<execution_time>\d+\.?\d*) s"
                r"\s*ClockTime = (?P<clock_time>\d+\.?\d*) s"
            ),
            single_value=True,
        )

    def _analyzer_date_and_hour(self):
        self.header_analyser.add_regex(
            r"^Date\s+:\s*(?P<date>\w\w\w \d\d \d\d\d\d)", single_value=True
        )
        self.header_analyser.add_regex(
            r"^Time\s+:\s*(?P<time>\d\d:\d\d:\d\d)", single_value=True
        )

    def _analyzer_number_processors(self):
        self.header_analyser.add_numeric_regex(
            r"^nProcs\s+:\s+(?P<nProcs>\d+)", single_value=True
        )
