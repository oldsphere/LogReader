from LogReader.checkmeshLog import checkmeshLog

from os.path import dirname

CURDIR = dirname(__file__)
LOGPATH = f"{CURDIR}/logs/checkMesh.log"


def test_parse():
    parser = checkmeshLog()
    out = parser.parse(LOGPATH)

    assert len(out) == 1
    time_zero_check = out[0]

    assert time_zero_check.nCells == 81710
    assert time_zero_check.patches == ["walls", "cylinder"]
    assert time_zero_check.maxNonOrthogonality == 40.8729
    assert time_zero_check.maxSkewness == 0.453296
