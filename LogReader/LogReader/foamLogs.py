from .LogAnalyzer import LogAnalyzer
from .content import clip, read_content

class snappyLog:
    def __init__(self):
        self.analyzer = LogAnalyzer()
        self.create_analyzers()

    def create_analyzers(self):
        """ Create SnappyHexMesh analyzers """
        self.analyzer.add_numeric_regex(
            r"Finished meshing in = (?P<meshing_time>\d+\.?\d*) s",
            single_value=True
        )

    def parse(self, filepath:str) -> dict:
        content = read_content(filepath)
        return self.analyzer.parse(content)
