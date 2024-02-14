from LogReader.LineAnalyzer import LineAnalyzer


elapsedTimeAnalyzer = LineAnalyzer(
    name="Elapsed Time",
    precondition=r'mimimi',
    condition=r"^Finished meshing in = (?P<elapedTime>\d+\.\d?) s",
    endcondition=r'end mimimi'
)

elapsedTimeAnalyzer.parse('mimimi')
print(
    elapsedTimeAnalyzer.parse('Finished meshing in = 27.5 s')
)
elapsedTimeAnalyzer.parse('end mimimi')
print(
    elapsedTimeAnalyzer.parse('Finished meshing in = 27.5 s')
)


