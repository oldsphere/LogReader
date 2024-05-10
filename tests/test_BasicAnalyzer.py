from LogReader.LogAnalyzer import BasicAnalyzer
from LogReader.LineAnalyzer import LineAnalyzer

CONTENT = (
    "This is the content\n"
    "Of the file information, with que followind data\n"
    "data: 23\n"
    "----\n"
    "Data: 12\n"
    "data: 10\n"
    "  data: 20\n"
    "data: 30\n"
    "data: 40\n"
    "And that is all"
)

def test_add_analyzer():
    analyzer = BasicAnalyzer()
    liner = LineAnalyzer(name='test', condition=r'mimi')
    assert len(analyzer.analyzers) == 0
    analyzer.add_analyzer(liner)
    assert len(analyzer.analyzers) == 1
    assert analyzer.analyzers[0] == liner


def test_parse():
    analyzer = BasicAnalyzer()
    liner = LineAnalyzer(name='test', condition=r'^data: (?P<data>\d+)$')
    analyzer.add_analyzer(liner)

    out = analyzer.parse(CONTENT)
    assert len(out['test']['data']) == 4
    assert out['test']['data'][1] == '10'
    assert out['test']['data'][2] == '30'
                         


def test_reset():
    analyzer = BasicAnalyzer()
    conditioned_liner = LineAnalyzer(
        name='test',
        precondition=r'^-+$',
        condition=r'^data: (?P<data>\d+)$',
        endcondition=r'^-+$',
    )
    liner = LineAnalyzer(name='test2', condition=r'^data: (?P<data>\d+)$')
    analyzer.add_analyzer(conditioned_liner)
    analyzer.add_analyzer(liner)

    assert (conditioned_liner.enabled == False and liner.enabled == True)
    out = analyzer.parse(CONTENT)
    print(out)
    assert (conditioned_liner.enabled == True and liner.enabled == True)

    analyzer.reset()
    assert (conditioned_liner.enabled == False and liner.enabled == True)
