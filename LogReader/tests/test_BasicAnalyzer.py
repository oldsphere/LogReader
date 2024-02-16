from LogReader.LogAnalyzer import BasicAnalyzer
from LogReader.LineAnalyzer import LineAnalyzer, TypeLineAnalyzer


def test_add_analyzer():
    basic = BasicAnalyzer()
    liner = LineAnalyzer(name="test", condition="mimi")
    basic.add_analyzer(liner)

    assert liner in basic.analyzer.analyzers


def test_add_numeric_regex():
    basic = BasicAnalyzer()
    pattern = r"First number: (?P<first>\d+) Second Number: (?P<second>\d+\.?\d*)"
    basic.add_numeric_regex(pattern)

    liner  = TypeLineAnalyzer(name='test', condition=pattern, conversor=(float, float))

    assert basic.analyzer.analyzers[0].condition == liner.condition
    assert basic.analyzer.analyzers[0].conversors == liner.conversors

def test_add_regex():
    basic = BasicAnalyzer()
    pattern = r"First number: (?P<first>\d+) Second Number: (?P<second>\d+\.?\d*)"
    basic.add_regex(pattern)

    assert basic.analyzer.analyzers[0].condition == pattern
