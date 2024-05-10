from LogReader.solverLog import parse_custom_expression, solverLog, parse_regex_file
from LogReader.content import read_content

from os.path import dirname

CURDIR = dirname(__file__)
LOGPATH = f"{CURDIR}/logs/rhoSimpleFoam_multirun.log"
REGEXPATH = f"{CURDIR}/logs/customRegExp"

floatFmt = r"-?\d+\.?\d*[eE]?[-+]?\d*"


def test_split_runs():
    parser = solverLog()

    content = read_content(LOGPATH)
    out = parser._split_runs(content)

    assert len(out) == 4


def test_split_time():
    parser = solverLog()

    content = read_content(LOGPATH)
    out = parser._split_runs(content)
    times = parser._split_time(out[1].content)

    print(times[1].content)

    assert len(times) == 474
    assert len(times[1].content.split("\n")) == 31
    assert times[1].name == "1"


def test_add_solving_field():
    parser = solverLog()
    parser.add_solving_field("myField")
    lineParser = parser.body_analyser.analyzers[-1]

    line = (
        "DILUPBiCGStab:  Solving for myField,"
        "Initial residual = 0.51395838,"
        "Final residual = 0.00038539459,"
        "No Iterations 1"
    )
    out = lineParser.parse(line)
    assert out["myField_initial_residual"] == 0.51395838


def test_parse_run():
    parser = solverLog()
    parser.add_solving_field("Ux")
    parser.add_solving_field("Uy")
    content = read_content(LOGPATH)
    run_clips = parser._split_runs(content)
    out = parser._parse_run(run_clips[1])

    assert len(out.execution_time.time) == 472
    assert out.execution_time.value[-1] == 38530.46
    assert len(out.Ux.time) == 473
    assert len(out.Ux.nIterations) == 473


def test_parse_regex_file():
    out = parse_regex_file(REGEXPATH)
    assert out[0].name == "pressureDrop"
    assert (
        out[0].condition == rf"areaAverage\(inlet\) of p = (?P<pressureDrop>{floatFmt})"
    )


def test_parse_custom_expression():
    expression = r'"areaAverage\(outlet\) of T = (%f%)"'
    new_expression, conversors = parse_custom_expression(
        name="test", expression=expression
    )
    assert new_expression == rf"areaAverage\(outlet\) of T = (?P<test>{floatFmt})"
    assert conversors == (float,)

    # Check failure by no float
    expression = '"Failure because non file"'
    try:
        new_expression, conversors = parse_custom_expression(
            name="test", expression=expression
        )
        raise AssertionError("Expresions without float does not raise error")
    except:
        pass

    # Check failure by multiple float
    expression = '"This fail (%f%) for (%f%) multiple matches"'
    try:
        new_expression, conversors = parse_custom_expression(
            name="test", expression=expression
        )
        raise AssertionError("Expresions with multiple float does not raise error")
    except:
        pass
