from os import read
from LogReader.LogAnalyzer import LogAnalyzer, read_content
from LogReader.LineAnalyzer import LineAnalyzer


# Defined the rules to analyze the log
layerPropsAnalyzer = LineAnalyzer(
    name="Layer Properties",
    precondition=r"patch\s*faces\s*layers\s*overall\s*thickness",
    condition=(
        r"^(?P<patchname>\w+)\s*"
        r"(?P<nFaces>\d+)\s*"
        r"(?P<nLayers>\d+)\s*"
        r"(?P<thickness>\d+)\s*"
        r"(?P<thickessFraction>\d+\.?\d*)\s*"
    ),
    endcondition=r"^\s*$",
)

elapsedTimeAnalyzer = LineAnalyzer(
    name="Elapsed Time",
    condition=r"Finished meshing in = (?P<elapedTime>\d+\.\d?)",
)

nonOrthogonalAnalyzer = LineAnalyzer(
    name="nonOrthogonal",
    condition=r"Mesh non-orthogonality Max: (?P<maxNonOrthogonality>\d+\.?\d*)",
)
meshStatsAnalyzer = LineAnalyzer(
    name="cells",
    condition=r"cells:\s*(?P<cells>\d+)"
)

# Generate and setting the Log file analyzer
snappyAnalyzer = LogAnalyzer()
snappyAnalyzer.add_analyzer(layerPropsAnalyzer)
snappyAnalyzer.add_analyzer(elapsedTimeAnalyzer)

checkMeshAnalyzer = LogAnalyzer()
checkMeshAnalyzer.add_analyzer(nonOrthogonalAnalyzer)
checkMeshAnalyzer.add_analyzer(meshStatsAnalyzer)

# Process the file
content = read_content("../logs/snappyHexMesh.log")
results = snappyAnalyzer.analyze(content)
print(results)

content = read_content("../logs/checkMesh.log")
results = checkMeshAnalyzer.analyze(content)
print(results)
