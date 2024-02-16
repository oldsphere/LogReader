from typing import List


def read_content(filepath: str) -> str:
    with open(filepath, "r") as fid:
        content = fid.read()
    return content


class ClipContent:
    def __init__(self, condition: str, endcondition: str = ""):
        """Constructor"""
        self.condition = condition
        self.endcondition = endcondition

    def apply(self, content: str) -> List[str]:
        return []
