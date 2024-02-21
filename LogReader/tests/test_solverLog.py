from LogReader.solverLog import solverLog
from LogReader.content import read_content

from os.path import dirname

CURDIR = dirname(__file__)
LOGPATH = f"{CURDIR}/logs/rhoSimpleFoam_multirun.log"


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


def test_parse_run():

    parser = solverLog()
    content = read_content(LOGPATH)
    run_clips = parser._split_runs(content)

    out = parser._parse_run(run_clips[1])

    assert len(out.execution_time.time) == 473
    assert out.execution_time.value[-1] == 38530.46
