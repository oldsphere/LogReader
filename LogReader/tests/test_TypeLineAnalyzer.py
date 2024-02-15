from LogReader.LineAnalyzer import TypeLineAnalyzer


def test_match_conversor():
    analyzer = TypeLineAnalyzer(
        name="test", 
        condition=r"name: (?P<name>\w+).*age: (?P<age>\d+)",
        conversor=(str,int)
    )

    assert analyzer.conversors['name'] == str
    assert analyzer.conversors['age'] == int


def test_simple_parse():
    analyzer = TypeLineAnalyzer(
        name="test", 
        condition=r"name: (?P<name>\w+).*age: (?P<age>\d+)",
        conversor=(str,int)
    )

    out = analyzer.parse("My name in Charles and mi age is 27")
    assert out == {}

    out = analyzer.parse("name: Charles age: 27")
    assert out["name"] == "Charles"
    assert out["age"] == 27

