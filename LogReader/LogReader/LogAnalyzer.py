from typing import List, Dict, Any, Callable
from .LineAnalyzer import LineAnalyzer, LineAnalyzerResult, TypeLineAnalyzer
import re

DictPattern = str


class LogAnalyzer:
    def __init__(self):
        self.analyzers = list()

    def add_analyzer(self, analyer: LineAnalyzer) -> None:
        self.analyzers.append(analyer)

    def parse(self, content: str) -> Dict[str, Any]:
        analyzer_results = {
            analyzer: LineAnalyzerResult() for analyzer in self.analyzers
        }
        for line in content.split("\n"):
            for analyzer in self.analyzers:
                out = analyzer.parse(line)
                if out:
                    analyzer_results[analyzer].add(out)

        return {
            analyzer.name: result.get_data()
            for analyzer, result in analyzer_results.items()
        }


class BasicAnalyzer:
    def __init__(self):
        self.analyzer = LogAnalyzer()

    def add_analyzer(self, analyzer: LineAnalyzer) -> None:
        self.analyzer.add_analyzer(analyzer)

    def add_numeric_regex(self, pattern: DictPattern) -> None:
        lineAnalyzerName = f"numeric_regex_{len(self.analyzer.analyzers)}"
        rePattern = re.compile(pattern)
        lineConversors = [float] * len(rePattern.groupindex.keys())
        lineAnalyzer = TypeLineAnalyzer(
            name=lineAnalyzerName, condition=pattern, conversor=lineConversors
        )
        self.analyzer.add_analyzer(lineAnalyzer)

    def add_regex(self, pattern: DictPattern) -> None:
        lineAnalyzerName = f"numeric_regex_{len(self.analyzer.analyzers)}"
        lineAnalyzer = LineAnalyzer(
            name=lineAnalyzerName,
            condition=pattern,
        )
        self.analyzer.add_analyzer(lineAnalyzer)
        
