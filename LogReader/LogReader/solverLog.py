from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer
from .content import read_content, clip, ClipContent

from typing import List, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime, time


@dataclass
class TimeSerie:
    time: List[float] = field(default_factory=list, repr=False)
    value: List[float] = field(default_factory=list, repr=False)

    def __repr__(self) -> str:
        nElements = len(self.time)
        minTime, maxTime = min(self.time), max(self.time)
        minVal, maxVal = min(self.value), max(self.value)
        return f"<TimeSerie nElements={nElements} time={minTime}:{maxTime} value={minVal}:{maxVal}>"


class FieldSolvingData:

    def __init__(self, name: str) -> None:
        self.name = name
        self.time = []
        self.initial_residual = []
        self.final_residual = []
        self.nIterations = []

    def add(self, time: float, initial: float, final: float, nIter: int) -> None:
        self.time.append(time)
        self.initial_residual.append(initial)
        self.final_residual.append(final)
        self.nIterations.append(nIter)

    def __repr__(self):
        return f"<FieldSolvingData field={self.name} ({len(self.time)})>"

    def has_valid_field(self, result:dict) -> bool:
        return all([
            'time' in result.keys(),
            f'{self.name}_initial_result' in result.keys(),
            f'{self.name}_final_result' in result.keys(),
            f'{self.name}_iterations' in result.keys(),
        ])

@dataclass
class solverLogData:
    date: datetime = datetime(1900, 1, 1)

    @classmethod
    def create_from_header(cls, header) -> "solverLogData":
        out = cls(date=cls._prepare_output_time(header))
        [out.add_attribute(name, value) for name, value in header.items()]
        return out

    @classmethod
    def extract_time_series(cls, out: List[dict]) -> Dict[str, TimeSerie]:

        def extract_single_time(globalDict: dict, timeDict: dict) -> None:
            time = timeDict.pop("time")

            for name, value in timeDict.items():
                # Add solving field data 


                # Ignore list values
                if type(value) == list:
                    continue

                # Add Time series data
                if not globalDict.get(name):
                    globalDict[name] = TimeSerie()
                globalDict[name].time.append(time)
                globalDict[name].value.append(value)

        timeSeries = {}
        [extract_single_time(timeSeries, time_match) for time_match in out]
        return timeSeries

    def add_time_series(self, series_data: list) -> None:
        series = self.extract_time_series(series_data)
        for name, value in series.items():
            self.add_attribute(name, value)

    def add_attribute(self, name: str, value: Any) -> None:
        setattr(self, name, value)

    @classmethod
    def _prepare_output_time(cls, out: dict) -> datetime:
        strDatetime = f"{out['date']} {out['time']}"
        return datetime.strptime(strDatetime, "%b %d %Y %H:%M:%S")


class solverLog:
    def __init__(self):
        self.body_analyser = LogAnalyzer()
        self.header_analyser = LogAnalyzer()
        self.create_analyzers()

    def create_analyzers(self):
        # Header Analyzers
        self._analyzer_date_and_hour()
        self._analyzer_number_processors()
        self._analyzer_solver_type()
        # Body Analyzers
        self._analyzer_execution_time()

    def parse(self, filepath: str) -> List[solverLogData]:
        full_content = read_content(filepath)
        run_content = self._split_runs(full_content)
        data = []
        for run in run_content[1:]:
            data.append(self._parse_run(run))
        return data

    def add_solving_field(self, field: str) -> None:
        self.body_analyser.add_numeric_regex(
            pattern=(
                rf"Solving for {field},\s*"
                rf"Initial residual = (?P<{field}_initial_residual>\d+\.?\d*),\s*"
                rf"Final residual = (?P<{field}_final_residual>\d+\.?\d*),\s*"
                rf"No Iterations (?P<{field}_iterations>\d+)"
            )
        )

    def _parse_header(self, header: ClipContent) -> dict:
        return self.header_analyser.parse(header.content)

    def _parse_iteration(self, iteration: ClipContent) -> dict:
        out = self.body_analyser.parse(iteration.content)
        out["time"] = float(iteration.name)
        return out

    def _parse_run(self, run_content: ClipContent) -> solverLogData:
        iterations = self._split_time(run_content.content)

        headerOut = self._parse_header(iterations.pop(0))

        results = solverLogData.create_from_header(headerOut)
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

    def _analyzer_solver_type(self):
        self.header_analyser.add_regex(
            r"Exec\s+:\s+(?P<solver_type>.+)", single_value=True
        )
