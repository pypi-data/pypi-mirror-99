# Cloudmesh Common


[![image](https://img.shields.io/pypi/v/cloudmesh-common.svg)](https://pypi.org/project/cloudmesh-common/)
[![Python](https://img.shields.io/pypi/pyversions/cloudmesh-common.svg)](https://pypi.python.org/pypi/cloudmesh-common)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/cloudmesh/cloudmesh-common/blob/main/LICENSE)
[![Format](https://img.shields.io/pypi/format/cloudmesh-common.svg)](https://pypi.python.org/pypi/cloudmesh-common)
[![Status](https://img.shields.io/pypi/status/cloudmesh-common.svg)](https://pypi.python.org/pypi/cloudmesh-common)
[![Travis](https://travis-ci.com/cloudmesh/cloudmesh-common.svg?branch=main)](https://travis-ci.com/cloudmesh/cloudmesh-common)


## Installation and Documentation

Please note that several packages are available which are pointed to in the
installation documentation.

|  | Links |
|---------------|-------|
| Documentation | <https://cloudmesh.github.io/cloudmesh-cloud> |
| Code | <https://github.com/cloudmesh/cloudmesh-cloud> |
| Installation Instructions | <https://github.com/cloudmesh/get> |

## Highlighted features

This library contains a number of useful functions and APIs that we highlight
here. They are used to interact with the system and provide a number of
functions to implement command line programs and shells.

## Console

The console provides convenient way to print colored messages types in the
terminal, such as errors, info, and regular messages

* [cloudmesh.common.console](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/console.py)

```python
from cloudmesh.common.console import Console

Console.error("this is an error printed in red wth prefix ERROR:")
Console.msg("this is a msg printed in black")
Console.ok("this is an ok message printed in green")
``` 

## Shell

We have lots of shell commands that call linux commands, but also have a
convenient execution command that returns the results in a string.

For more information we like you to inspect the source code:

* [cloudmesh.common.Shell](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/Shell.py)


```python
from cloudmesh.common.Shell import Shell

shell = Shell()

print(shell.terminal_type())

# prints after the command is finished
r = shell.execute('pwd') 
print(r)

# prints while the command is executed
r = shell.live('pwd') 
print(r)

# open a new terminal and start the command ls in it (for OSX and Gnome)
shell.terminal("ls")

# an example of a build in command
shell.pip("install cloudmesh-common")
```
 
We have many such build in commands, please see the source

    
## Printer

A convenient way to print dictionaries and lists with repeated
entries as tables, csv, json, yaml. The dictionaries can even be hierarchical.

* [cloudmesh.common.Printer](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/Printer.py)

Let us assume we have 

```python
data = [
    {
        "name": "Gregor",
        "address": {
            "street": "Funny Lane 11",
            "city": "Cloudville"
        {
    },
    {
        "name": "Albert",
        "address": {
            "street": "Memory Lane 1901",
            "city": "Cloudnine"
        }
    }
]
```

Then we can print it nicely with 

```python
print(Printer.flatwrite(self.data,
                    sort_keys=["name"],
                    order=["name", "address.street", "address.city"],
                    header=["Name", "Street", "City"],
                    output="table")
          )
```

Other formats such as csv, json, dict are also supported.

In addition we have also printers for printing attribute lists. Please consult
the source code.

## StopWatch

See: https://colab.research.google.com/drive/1tG7IcP-XMQiNVxU05yazKQYciQ9GpMat#scrollTo=TZAjATZiQh4q&uniqifier=1 for an example

### Using Cloudmesh StopWatch Inline

```python
from cloudmesh.common.StopWatch import StopWatch
import time

StopWatch.start("a")

time.sleep(3)

StopWatch.stop("a")

StopWatch.status("a", True)

StopWatch.benchmark()
```

### Using Cloudmesh Benchmark wrapped in Functions

If it is not wrapped in functions, do not use it this way.

``` python
from cloudmesh.common.Benchmark import Benchmark
import time
  
def b():
  Benchmark.Start()
  time.sleep(3)
  Benchmark.Stop()

def c():
  Benchmark.Start()
  time.sleep(1)
  Benchmark.Stop()

 b()
 c()

Benchmark.print()
```

* See also: [cloudmesh.common.StopWatch](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/StopWatch.py)

    

## dotdict


* [cloudmesh.common.dotdict](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/dotdict.py)

One dimensional Dictionaries in dot format. 

```python
from cloudmesh.common.dotdict import doctict

# convert a simple dict to a dotdict
d = dotdict({"name": "Gregor"})
# Now you can say
print(d["name"])
print(d.name)
```

## ssh

* [cloudmesh.common.ssh](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/ssh)

  * managing ssh config files
  * managing authorized keys

## util

Very useful functions are included in util


* [cloudmesh.common.util](https://github.com/cloudmesh/cloudmesh-common/blob/main/cloudmesh/common/util.py)

Especially useful are

  * generating passwords
  * banners
  * yn_choices
  * path_expansion
  * grep (simple line matching)
  * HEADING() which without parameter identifies the name of the function and 
  prints its name within a banner

## Changes

* added support for terminals with dark background
