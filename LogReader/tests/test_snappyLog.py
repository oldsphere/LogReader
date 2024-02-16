from os.path import dirname
from LogReader.foamLogs import snappyLog    

def test_parse():
    curdir = dirname(__file__)
    logPath = f'{curdir}/logs/snappyHexMesh.log'

    parser = snappyLog()
    out = parser.parse(logPath)

    assert out['meshing_time'] == 13.25
