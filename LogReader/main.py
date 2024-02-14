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

# Generate and setting the Log file analyzer
snappyAnalyzer = LogAnalyzer()
snappyAnalyzer.add_analyzer(layerPropsAnalyzer)
snappyAnalyzer.add_analyzer(elapsedTimeAnalyzer)

# Process the file
content = read_content('../logs/snappyHexMesh.log')
results = snappyAnalyzer.analyze(content)

# Access the results
print(results)
