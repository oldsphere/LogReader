from os.path import dirname
from LogReader.foamLogs import snappyLog    
from datetime import datetime

def test_parse():
    curdir = dirname(__file__)
    logPath = f'{curdir}/logs/snappyHexMesh.log'

    parser = snappyLog()
    out = parser.parse(logPath)

    print(out)
    assert out.meshing_time == 13.25
    assert out.date == datetime(2024, 2, 12, 20, 2, 43)
    assert out.bbox.xmin == -10
    assert out.layers[0].nFaces == 2400
