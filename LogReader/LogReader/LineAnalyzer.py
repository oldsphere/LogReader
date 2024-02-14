import re


class LineAnalyzer:
    """Line Analyzer"""

    def __init__(
        self,
        name: str,
        condition: str,
        precondition: str = "",
        endcondition: str = "",
    ) -> None:
        self.name = name
        self.condition = condition
        self.precondition = precondition
        self.endcondition = endcondition

        self.enabled = False if precondition else True

    def set_state(self, new_state: bool) -> None:
        self.enabled = new_state

    def update_state(self, line: str) -> None:
        if not self.precondition:
            return
        matches = re.search(self.precondition, line)
        if matches and not self.enabled:
            self.enabled = True
            return

        if not self.endcondition:
            return
        matches = re.search(self.endcondition, line)
        if matches and self.enabled:
            self.enabled = False
            return

    def parse(self, line: str) -> dict:
        self.update_state(line)
        match = re.search(self.condition, line)
        if match and self.enabled:
            return match.groupdict()
        return {}


class LineAnalyzerResult:
    def __init__(self):
        self.data = dict()

    def add(self, new_data: dict):
        for k, v in new_data.items():
            if not k in self.data.keys():
                self.data[k] = [v]
                continue
            self.data[k].append(v)

    def get_data(self) -> dict:
        return self.data
