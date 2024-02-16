from LogReader.LogAnalyzer import LogAnalyzer
from LogReader.LineAnalyzer import LineAnalyzer

def test_add_analyzer():
    analyzer = LogAnalyzer()
    liner = LineAnalyzer(name='test', condition=r'mimi')
    assert len(analyzer.analyzers) == 0
    analyzer.add_analyzer(liner)
    assert len(analyzer.analyzers) == 1
    assert analyzer.analyzers[0] == liner


def test_analyze():
    analyzer = LogAnalyzer()
    liner = LineAnalyzer(name='test', condition=r'^data: (?P<data>\d+)$')
    analyzer.add_analyzer(liner)

    content = (
        "This is the content\n"
        "Of the file information, with que followind data\n"
        "Data: 12\n"
        "data: 10\n"
        "  data: 20\n"
        "data: 30\n"
        "data: 40\n"
        "And that is all"
    )

    out = analyzer.parse(content)
    assert len(out['test']['data']) == 3
    assert out['test']['data'][0] == '10'
    assert out['test']['data'][1] == '30'
                         



