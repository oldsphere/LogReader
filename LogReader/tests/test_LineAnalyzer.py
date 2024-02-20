from LogReader.LineAnalyzer import LineAnalyzer


def test_simple_parse():
    analyzer = LineAnalyzer(
        name="test", condition=r"name: (?P<name>\w+).*age: (?P<age>\d+)"
    )

    out = analyzer.parse("My name in Charles and mi age is 27")
    assert out == {}

    out = analyzer.parse("name: Charles age: 27")
    assert out["name"] == "Charles"
    assert out["age"] == "27"


def test_set_state():
    analyzer = LineAnalyzer(name="test", condition="")
    assert analyzer.enabled == True, "Initialy enabled"
    analyzer.set_state(False)
    assert analyzer.enabled == False
    analyzer.set_state(True)
    assert analyzer.enabled == True


def test_condition_parse():
    analyzer = LineAnalyzer(
        name="test",
        precondition=r"Data:",
        condition=r"name: (?P<name>\w+).*age: (?P<age>\d+)",
        endcondition="End Data",
    )

    assert analyzer.enabled == False

    out = analyzer.parse("My name in Charles and mi age is 27")
    assert analyzer.enabled == False
    assert out == {}

    out = analyzer.parse("Data:")
    assert analyzer.enabled == True
    assert out == {}

    out = analyzer.parse("random content")
    assert analyzer.enabled == True
    assert out == {}

    out = analyzer.parse("name: Charles age: 27")
    assert analyzer.enabled == True
    assert out["name"] == "Charles"
    assert out["age"] == "27"

    out = analyzer.parse("End Data")
    assert analyzer.enabled == False

    out = analyzer.parse("name: Charles age: 27")
    assert analyzer.enabled == False
    assert out == {}

    out = analyzer.parse("sdjskldjskl")
    assert analyzer.enabled == False
    assert out == {}


def test_reset():
    analyzer = LineAnalyzer(
        name="test",
        precondition=r"Data:",
        condition=r"name: (?P<name>\w+).*age: (?P<age>\d+)",
        endcondition="End Data",
    )

    assert analyzer.enabled == False

    analyzer.set_state(True)
    analyzer.reset()

    assert analyzer.enabled == False
