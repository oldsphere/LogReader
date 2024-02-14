from PyFoam.Execution.BasicWatcher import BasicWatcher
from PyFoam.Execution.StepAnalyzedCommon import StepAnalyzedCommon
from PyFoam.LogAnalysis.BoundingLogAnalyzer import BoundingLogAnalyzer

class LogReader(BasicWatcher, StepAnalyzedCommon):
    def __init__(self, filename):
        BasicWatcher.__init__(self, filename, follow=False, silent=True)

        analyzer = BoundingLogAnalyzer()

        StepAnalyzedCommon.__init__(
            self,
            filename,
            analyzer,
            writePickled=False,
        )



