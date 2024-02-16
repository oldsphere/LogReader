from LogReader.content import read_content
from LogReader.LogAnalyzer import LogAnalyzer
from LogReader.LineAnalyzer import LineAnalyzer, TypeLineAnalyzer


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

nonOrthogonalAnalyzer = TypeLineAnalyzer(
    name="nonOrthogonal",
    condition=r"Mesh non-orthogonality Max: (?P<maxNonOrthogonality>\d+\.?\d*)",
    conversor=(float,)
)
meshStatsAnalyzer = TypeLineAnalyzer(
    name="cells",
    condition=r"cells:\s*(?P<cells>\d+)",
    conversor=(int,)
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
results = snappyAnalyzer.parse(content)
print(results)

content = read_content("../logs/checkMesh.log")
results = checkMeshAnalyzer.parse(content)
print(results)
