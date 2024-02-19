from .LogAnalyzer import LogAnalyzer
from .LineAnalyzer import TypeLineAnalyzer

from typing import List
from .content import clip, read_content
from dataclasses import dataclass, field
from datetime import datetime
from collections import namedtuple

bboxType = namedtuple("Bbox", ["xmin", "xmax", "ymin", "ymax", "zmin", "zmax"])


@dataclass
class snappyLayerData:
    name: str
    nFaces: int
    nLayers: int
    thickess: float
    fraction: float


@dataclass
class snappyLogData:
    date: datetime
    nProcs: int = field(repr=False)
    bbox: bboxType = field(repr=False)
    meshing_time: float
    layers: List[snappyLayerData]


class snappyLog:
    def __init__(self):
        self.analyzer = LogAnalyzer()
        self.create_analyzers()

    def create_analyzers(self):
        self._analyzer_number_processors()
        self._analyzer_mesh_bounding_box()
        self._analyzer_date_and_hour()
        self._analyzer_mesing_time()
        self._analyzer_layer_properties()

    def parse(self, filepath: str) -> snappyLogData:
        content = read_content(filepath)
        out = self.analyzer.parse(content)
        outResult = self.prepare_output(out)
        return outResult

    def prepare_output(self, out: dict) -> snappyLogData:
        return snappyLogData(
            date=self._prepare_output_time(out),
            nProcs=out["nProcs"],
            bbox=self._prepare_output_bbox(out),
            meshing_time=out["meshing_time"],
            layers=self._prepare_output_layers(out),
        )

    def _prepare_output_layers(self, out: dict) -> List[snappyLayerData]:
        if not out.get("layer_patchname"):
            return []
        layerOutData = zip(
            out["layer_patchname"],
            out["layer_nFaces"],
            out["layer_nLayers"],
            out["layer_thickness"],
            out["layer_thicknessFraction"],
        )
        return [
            snappyLayerData(name, nFaces, nLayers, thickness, fraction)
            for name, nFaces, nLayers, thickness, fraction in layerOutData
        ]

    def _prepare_output_time(self, out: dict) -> datetime:
        strDatetime = f"{out['date']} {out['time']}"
        return datetime.strptime(strDatetime, "%b %d %Y %H:%M:%S")

    def _prepare_output_bbox(self, out: dict) -> bboxType:
        return bboxType(
            out["xmin"], out["xmax"], out["ymin"], out["ymax"], out["zmin"], out["zmax"]
        )

    def _analyzer_mesh_bounding_box(self):
        boundingBoxAnalyzer = TypeLineAnalyzer(
            name="boundingBox",
            condition=(
                r"Overall mesh bounding box\s*:\s"
                r"\((?P<xmin>-?\d+\.?\d*) "
                r"(?P<ymin>-?\d+\.?\d*) "
                r"(?P<zmin>-?\d+\.?\d*)\)"
                r"\s*\((?P<xmax>-?\d+\.?\d*) "
                r"(?P<ymax>-?\d+\.?\d*) "
                r"(?P<zmax>-?\d+\.?\d*)\)"
            ),
            conversor=(float, float, float, float, float, float),
        )
        self.analyzer.add_analyzer(boundingBoxAnalyzer, single_value=True)

    def _analyzer_number_processors(self):
        self.analyzer.add_numeric_regex(
            r"^nProcs\s+:\s+(?P<nProcs>\d+)", single_value=True
        )

    def _analyzer_date_and_hour(self):
        self.analyzer.add_regex(
            r"^Date\s+:\s*(?P<date>\w\w\w \d\d \d\d\d\d)", single_value=True
        )
        self.analyzer.add_regex(
            r"^Time\s+:\s*(?P<time>\d\d:\d\d:\d\d)", single_value=True
        )

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
                r"(?P<layer_thicknessFraction>\d+\.?\d*)\s*"
            ),
            endcondition=r"^\s*$",
            conversor=(str, int, int, float, float),
        )
        self.analyzer.add_analyzer(layerPropsAnalyzer)
