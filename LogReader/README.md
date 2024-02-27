LogReader
================================================================================

## Description:
This is a module to read openfoam log files, based on the structure of pyfoam.
Is developed to personal use.

```python
from LogReader.checkmeshLog import checkmeshLog

parser = checkmeshLog()
out = parser.parse('case/logs/checkMesh.log')
print(out[0].maxNonOrthogonality)
```
