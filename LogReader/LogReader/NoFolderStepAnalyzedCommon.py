from PyFoam.Execution.AnalyzedCommon import AnalyzedCommon
from PyFoam.LogAnalysis.FoamLogAnalyzer import FoamLogAnalyzer
from PyFoam.LogAnalysis.ExecNameLineAnalyzer import ExecNameLineAnalyzer

class NoFolderAnalyzedCommon(AnalyzedCommon):

    def  __init__( self, filenames, analyzer:FoamLogAnalyzer):

        if type(filenames) is list:
            filename=filenames[0]
        else:
            filename=filenames

        self.analyzer=analyzer
        self.analyzer.addResetFileTrigger(self.resetFile)

        self.reset()

        self.persist=None
        self.start_=None
        self.end=None
        self.raiseit=False
        self.writeFiles=False
        self.splitThres=2048
        self.split_fraction_unchanged=0.2
        self.plottingImplementation="dummy"
        self.gnuplotTerminal=None

        eName=ExecNameLineAnalyzer()
        eName.addListener(self.execNameFound)
        self.addAnalyzer("ExecName",eName)
        self.automaticCustom=None

        self.tickers=[]
        self.plots={}


class NoFolderStepAnalyzedCommon(NoFolderAnalyzedCommon):

    def __init__(self):
        ...
