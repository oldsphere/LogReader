from .LineAnalyzer import LineAnalyzer, LineAnalyzerResult, TypeLineAnalyzer
import re
from typing import Dict, Any

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
        """Add and externally defined analyzer"""
        self.analyzer.add_analyzer(analyzer)

    def add_numeric_regex(self, pattern: DictPattern) -> None:
        """Add a analyzer and convert the matches to float"""
        lineAnalyzerName = f"numeric_regex_{len(self.analyzer.analyzers)}"
        rePattern = re.compile(pattern)
        lineConversors = [float] * len(rePattern.groupindex.keys())
        lineAnalyzer = TypeLineAnalyzer(
            name=lineAnalyzerName, condition=pattern, conversor=lineConversors
        )
        self.analyzer.add_analyzer(lineAnalyzer)

    def add_regex(self, pattern: DictPattern) -> None:
        """Add a analyzer and return the matches as str"""
        lineAnalyzerName = f"regex_{len(self.analyzer.analyzers)}"
        lineAnalyzer = LineAnalyzer(
            name=lineAnalyzerName,
            condition=pattern,
        )
        self.analyzer.add_analyzer(lineAnalyzer)

    def parse(self, content: str) -> dict:
        out = self.analyzer.parse(content)
        out = self.flat_results(out)
        print(out)
        return out

    @staticmethod
    def flat_results(out: dict) -> dict:
        """Reduce the nesting of out results"""
        if BasicAnalyzer.is_name_collision(out):
            raise Exception("There is name collision in the analyzers")
        final_out = {}
        for analyzerOut in out.values():
            final_out.update(analyzerOut)
        return final_out

    @staticmethod
    def is_name_collision(out: dict) -> bool:
        names = []
        for analyzerOut in out.values():
            names += list(analyzerOut.keys())
        return len(names) != len(set(names))
