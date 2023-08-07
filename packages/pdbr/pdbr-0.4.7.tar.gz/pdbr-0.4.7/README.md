# pdbr

[![PyPI version](https://badge.fury.io/py/pdbr.svg)](https://pypi.org/project/pdbr/) [![Python Version](https://img.shields.io/pypi/pyversions/pdbr.svg)](https://pypi.org/project/pdbr/) [![](https://github.com/cansarigol/pdbr/workflows/Test/badge.svg)](https://github.com/cansarigol/pdbr/actions?query=workflow%3ATest)

pdbr is intended to make the PDB results more colorful. it uses [Rich](https://github.com/willmcgugan/rich) library to carry out that.


## Installing

Install with `pip` or your favorite PyPi package manager.

```
pip install pdbr
```


## Breakpoint

In order to use ```breakpoint()```, set **PYTHONBREAKPOINT** with "pdbr.set_trace"

```python
import os

os.environ["PYTHONBREAKPOINT"] = "pdbr.set_trace"
```

or just import pdbr

```python
import pdbr
```

## New commands
### (v)ars
Get the local variables list as table.

### varstree | vt
Get the local variables list as tree.

### (i)nspect / inspectall | ia
[rich.inspect](https://rich.readthedocs.io/en/latest/introduction.html?s=03#rich-inspector)

![](/images/image5.png)

### pp
[rich.pretty.pprint](https://rich.readthedocs.io/en/latest/reference/pretty.html?highlight=pprint#rich.pretty.pprint)
### (ic)ecream
🍦 [Icecream](https://github.com/gruns/icecream) print.
### nn, ss, uu, dd
Same with n(ext), s(tep), u(p), d(own) commands + with local variables.

![](/images/image8.png)

## Config
### Style
In order to use Rich's traceback, style, and theme, set **setup.cfg**.

```
[pdbr]
style = yellow
use_traceback = True
theme = friendly
```

### History
**store_history** setting is used to keep and reload history, even the prompt is closed and opened again.
```
[pdbr]
...
store_history=.pdbr_history
```

## Celery
In order to use **Celery** remote debugger with pdbr, use ```celery_set_trace``` as below sample. For more information see the [Celery user guide](https://docs.celeryproject.org/en/stable/userguide/debugging.html).

```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    
    import pdbr; pdbr.celery_set_trace()
    
    return x + y

```
#### Telnet
Instead of using `telnet` or `nc`, in terms of using pdbr style, `pdbr_telnet` command can be used.
![](/images/image6.png)


## IPython 

Being able to use [ipython](https://ipython.readthedocs.io/), install pdbr with it like below or just install your own version.

```
pip install pdbr[ipython]
```

## pytest
In order to user `pdbr` with pytest `--pdb` flag, add `addopts` setting in your pytest.ini.

```
[pytest]
addopts: --pdbcls=pdbr:RichPdb
```
### Shell
Running `pdbr` command in terminal starts an `IPython` terminal app instance. Unlike default `TerminalInteractiveShell`, the new shell uses pdbr as debugger class instead of `ipdb`.
#### %debug magic sample
![](/images/image9.png)
### Terminal
#### Django shell sample
![](/images/image7.png)

## Vscode user snippet

To create or edit your own snippets, select **User Snippets** under **File > Preferences** (**Code > Preferences** on macOS), and then select **python.json**. 

Place the below snippet in json file for **pdbr**.

```
{
  ...
  "pdbr": {
        "prefix": "pdbr",
        "body": "import pdbr; pdbr.set_trace()",
        "description": "Code snippet for pdbr debug"
    },
}
```

For **Celery** debug.

```
{
  ...
  "rdbr": {
        "prefix": "rdbr",
        "body": "import pdbr; pdbr.celery_set_trace()",
        "description": "Code snippet for Celery pdbr debug"
    },
}
```

## Samples
![](/images/image1.png)

![](/images/image3.png)

![](/images/image4.png)

### Traceback
![](/images/image2.png)
