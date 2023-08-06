pyasstosrt
=================================================================================================================================================================================

[![Build Status](https://travis-ci.com/GitBib/pyasstosrt.svg?branch=master)](https://travis-ci.com/GitBib/pyasstosrt) [![alt text](https://img.shields.io/pypi/v/pyasstosrt.svg?style=flat)](https://pypi.org/project/pyasstosrt/)

**pyasstosrt** – this tool will help you convert Advanced SubStation Alpha (ASS/SSA) subtitle files to SubRip (SRT) files.

Support for str path:
```python
from pyasstosrt import Subtitle

sub = Subtitle('sub.ass')
sub.export()
```

Support for all Path-like objects, instead of only pathlib's Path:

```python
from pathlib import Path

from pyasstosrt import Subtitle

path = Path('sub.ass')
sub = Subtitle(path)
sub.export()
```

CLI
------------
```bash
pyasstosrt --filepath=/Users/user/sub/sub.ass export
```

**Optional** You can specify an export folder.
```bash
pyasstosrt --filepath=/Users/user/sub/sub.ass export /Users/user/sub/srt
```

Installation
------------
Most users will want to simply install the latest version, hosted on PyPI:

    $ pip install pyasstosrt
