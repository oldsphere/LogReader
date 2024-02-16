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
        self.single_value_analyzers = []

    def add_analyzer(self, analyzer: LineAnalyzer, single_value: bool = False) -> None:
        """Add and externally defined analyzer"""
        self.analyzer.add_analyzer(analyzer)
        if single_value:
            self.single_value_analyzers.append(analyzer.name)

    def add_numeric_regex(
        self, pattern: DictPattern, single_value: bool = False
    ) -> None:
        """Add a analyzer and convert the matches to float"""
        lineAnalyzerName = f"numeric_regex_{len(self.analyzer.analyzers)}"
        rePattern = re.compile(pattern)
        lineConversors = [float] * len(rePattern.groupindex.keys())
        lineAnalyzer = TypeLineAnalyzer(
            name=lineAnalyzerName, condition=pattern, conversor=lineConversors
        )
        self.add_analyzer(lineAnalyzer, single_value)

    def add_regex(self, pattern: DictPattern, single_value: bool = False) -> None:
        """Add a analyzer and return the matches as str"""
        lineAnalyzerName = f"regex_{len(self.analyzer.analyzers)}"
        lineAnalyzer = LineAnalyzer(
            name=lineAnalyzerName,
            condition=pattern,
        )
        self.add_analyzer(lineAnalyzer, single_value)

    def parse(self, content: str) -> dict:
        out = self.analyzer.parse(content)
        out = self.single_results(out)
        print(out)
        out = self.flat_results(out)
        return out

    def single_results(self, out: dict) -> dict:
        singled_out = {}

        def single_dict(source: dict) -> dict:
            return {k: v[0] for k, v in source.items()}

        def is_dict_singlable(source: dict) -> bool:
            return all([len(v) == 1 for v in source.values()])

        for k, v in out.items():
            if k in self.single_value_analyzers:
                assert is_dict_singlable(v), "A single analyzer have multiple values"
                v = single_dict(v)
            singled_out[k] = v

        return singled_out

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
