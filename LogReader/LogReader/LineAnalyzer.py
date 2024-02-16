import re
from typing import Iterable, Callable

DictPattern = str
NullablePattern = str

class LineAnalyzer:
    """Line Analyzer"""

    def __init__(
        self,
        name: str,
        condition: DictPattern,
        precondition: NullablePattern = "",
        endcondition: NullablePattern = "",
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


class TypeLineAnalyzer(LineAnalyzer):
    def __init__(
        self,
        name: str,
        condition: DictPattern,
        conversor: Iterable[Callable],
        precondition: NullablePattern = "",
        endcondition: str = "",
    ) -> None:
        super().__init__(name, condition, precondition, endcondition)
        self.macth_conversors(conversor)

    def macth_conversors(self, conversors: Iterable[Callable]) -> None:
        field_pattern: str = r"\(\?P\<(.+)\>"
        fields = re.findall(field_pattern, self.condition)
        self.conversors = {
            field: conversor for field, conversor in zip(fields, conversors)
        }

    def parse(self, line: str) -> dict:
        out = super().parse(line)
        if out:
            out = { k:self.conversors[k](v) for k,v in out.items()}
            print(out)
        return out


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
