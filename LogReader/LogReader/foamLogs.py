from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer
from .content import clip, read_content


class snappyLog:
    def __init__(self):
        self.analyzer = LogAnalyzer()
        self.create_analyzers()

    def parse(self, filepath: str) -> dict:
        content = read_content(filepath)
        return self.analyzer.parse(content)

    def create_analyzers(self):
        self._analyzer_mesing_time()
        self._analyzer_layer_properties()

    def _analyzer_mesing_time(self):
        self.analyzer.add_numeric_regex(
            r"Finished meshing in = (?P<meshing_time>\d+\.?\d*) s", single_value=True
        )

    def _analyzer_layer_properties(self):
        layerPropsAnalyzer = TypeLineAnalyzer(
            name="Layer Properties",
            precondition=r"patch\s*faces\s*layers\s*overall\s*thickness",
            condition=(
                r"^(?P<layer_patchname>\w+)\s*"
                r"(?P<layer_nFaces>\d+)\s*"
                r"(?P<layer_nLayers>\d+)\s*"
                r"(?P<layer_thickness>\d+)\s*"
                r"(?P<layer_thickessFraction>\d+\.?\d*)\s*"
            ),
            endcondition=r"^\s*$",
            conversor=(str, int, int, float, float),
        )
        self.analyzer.add_analyzer(layerPropsAnalyzer)
