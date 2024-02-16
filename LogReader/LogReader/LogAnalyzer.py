from typing import List, Dict, Any
from .LineAnalyzer import LineAnalyzer, LineAnalyzerResult


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
            for analyzer,result in analyzer_results.items()
        }
