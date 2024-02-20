from LogReader.solverLog import solverLog
from LogReader.content import read_content

from os.path import dirname

CURDIR = dirname(__file__)
LOGPATH = f'{CURDIR}/logs/rhoSimpleFoam_multirun.log'

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
    assert len(times[1].content.split('\n')) == 31
    assert times[1].name == '1'

