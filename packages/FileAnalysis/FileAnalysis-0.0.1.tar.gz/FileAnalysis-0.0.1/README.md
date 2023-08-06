# FileAnalysis

## Description
This package analyze emergence of characters in file (to decrypt with statistics).

## Requirements
This package require :
 - python3
 - python3 Standard Library
 - matplotlib

## Installation
```bash
pip install FileAnalysis
```

## Launcher

## Command line:
```bash
FileAnalysis -h # Print help message
FileAnalysis -F # Show french emergence
FileAnalysis -f text.txt # Show all characters emergence in file named "text.txt"
FileAnalysis -a -f text.txt # Show alphabet characters emergence in file named "text.txt"
FileAnalysis -n -f text.txt # Show all characters emergence number (default show pourcent)
```

### Python script
```python
from FileAnalysis import FileAnalysis
analysis = FileAnalysis("text.txt", alphabet_only=True)
result = analysis.analysis_filecontent()
result = analysis.get_pourcent()
analysis.build_chart() # Show chart
```

### Python executable:
```bash
python3 FileAnalysis.pyz -f text.txt

# OR
chmod u+x FileAnalysis.pyz # add execute rights
./FileAnalysis.pyz -F # execute file
```

### Python module (command line):

```bash
python3 -m FileAnalysis -F
python3 -m FileAnalysis.FileAnalysis text.txt
```

## Links
 - [Github Page](https://github.com/mauricelambert/FileAnalysis)
 - [Documentation](https://mauricelambert.github.io/info/python/security/FileAnalysis.html)
 - [Download as python executable](https://mauricelambert.github.io/info/python/security/FileAnalysis.pyz)
 - [Pypi package](https://pypi.org/project/FileAnalysis/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
