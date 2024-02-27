from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer
from .content import read_content, clip, ClipContent

from dataclasses import dataclass, field
from typing import List


@dataclass
class checkMeshLogData:
    nCells: int
    maxNonOrthogonality: float
    maxSkewness: float
    patches: List[str] = field(default_factory=list)

    @classmethod
    def create_from_log(cls, results: dict) -> "checkMeshLogData":
        return cls(
            nCells=results.get("nCells", 0),
            maxNonOrthogonality=results.get("maxNonOrthogonality", 0.0),
            maxSkewness=results.get("maxSkewness", 0.0),
            patches=results.get("patch_name", []),
        )


class checkmeshLog:
    def __init__(self):
        self.analyzer = LogAnalyzer()
        self.create_analyzers()

    def create_analyzers(self):
        self._analyzer_mesh_stats()
        self._analyzer_patches()
        # self._analyzer_faceZones()
        # self._analyzer_cellZones()
        self._analyzer_quality()

    def parse(self, filepath: str) -> List[checkMeshLogData]:
        full_content = read_content(filepath)
        time_clips = self._split_by_time(full_content)
        header_clip = time_clips.pop(0)
        return [self._parse_time(time_clip) for time_clip in time_clips]

    def _parse_time(self, time_clip: ClipContent) -> checkMeshLogData:
        self.analyzer.reset()
        out = self.analyzer.parse(time_clip.content)
        out["time"] = float(time_clip.name)
        print(out)
        return checkMeshLogData.create_from_log(out)

    def _split_by_time(self, content: str) -> List[ClipContent]:
        return clip(clip_pattern=r"\nTime\s*=\s*(?P<time>\d\.?\d*)", content=content)

    def _analyzer_mesh_stats(self):
        ncells_analyzer = TypeLineAnalyzer(
            name="number_cell_analyzer",
            precondition=r"^Mesh stats$",
            condition=r"\s*cells:\s*(?P<nCells>\d+)",
            endcondition=r"^\s*$",
            conversor=(float,),
        )

        npoints_analyzer = TypeLineAnalyzer(
            name="number_points_analyzer",
            precondition=r"^Mesh stats$",
            condition=r"\s*points:\s*(?P<nPoints>\d+)",
            endcondition=r"^\s*$",
            conversor=(float,),
        )

        nfaces_analyzer = TypeLineAnalyzer(
            name="number_faces_analyzer",
            precondition=r"^Mesh stats$",
            condition=r"^\s*faces:\s*(?P<nFaces>\d+)",
            endcondition=r"^\s*$",
            conversor=(float,),
        )

        self.analyzer.add_analyzer(ncells_analyzer, single_value=True)
        self.analyzer.add_analyzer(nfaces_analyzer, single_value=True)
        self.analyzer.add_analyzer(npoints_analyzer, single_value=True)

    def _analyzer_patches(self):
        patch_analyzer = TypeLineAnalyzer(
            name="patches_regex",
            precondition=r"Checking patch topology for multiply connected surfaces...",
            condition=r"\s*(?P<patch_name>\w+)\s*\d+",
            endcondition=r"^\s*$",
            conversor=(str,),
        )
        self.analyzer.add_analyzer(patch_analyzer)

    def _analyzer_quality(self):
        maxNonOrthogonality_analyzer = TypeLineAnalyzer(
            name="maxNonOrthogonality_regex",
            precondition="Checking geometry...",
            condition=r"\s*Mesh non-orthogonality Max: (?P<maxNonOrthogonality>\d+\.\d*)",
            endcondition=r"^\s*$",
            conversor=(float,),
        )
        maxSkewness_analyzer = TypeLineAnalyzer(
            name="maxSkewness_regex",
            precondition="Checking geometry...",
            condition=r"\s*Max skewness = (?P<maxSkewness>\d+\.\d*)",
            endcondition=r"^\s*$",
            conversor=(float,),
        )
        self.analyzer.add_analyzer(maxNonOrthogonality_analyzer, single_value=True)
        self.analyzer.add_analyzer(maxSkewness_analyzer, single_value=True)
