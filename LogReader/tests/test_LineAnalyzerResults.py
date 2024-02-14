from LogReader.LineAnalyzer import LineAnalyzerResult


def test_add():

    analyzerResult = LineAnalyzerResult()

    analyzerResult.add({"time": 20})
    analyzerResult.add({"time": 40})

    data = analyzerResult.get_data()
    assert len(data['time']) == 2
    assert data['time'][0] == 20
    assert data['time'][1] == 40
