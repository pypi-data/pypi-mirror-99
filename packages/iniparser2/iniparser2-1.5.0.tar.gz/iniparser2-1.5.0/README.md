# iniparser2

[![Build Status](https://travis-ci.com/HugeBrain16/iniparser2.svg?branch=main)](https://travis-ci.com/HugeBrain16/iniparser2)  

**iniparser2** is An INI parser or a Config parser.  

this package is the improved version of [**iniparser**](https://github.com/HugeBrain16/iniparser) with more features.

---

# Quick Start

## Installation

to install the package see the following step below

from source: `python setup.py install`  

## Examples

**These examples below is for getting the value from the properties**
</br>
basic example

`test.ini`:
```ini
name=Mike Hawk
```

`test.py`:
```py
from iniparser2 import INI

x = INI('test.ini')
data = x.get()

print(data)
```

#### Output:
```py
{'name': 'Mike Hawk'}
```

using `with` keyword  

`test.ini`:
```ini
name=Mike Hawk
```
  
`test.py`:  
```py
from iniparser2 import INI

with INI('test.ini') as i:
    print(i.get())
```
#### Output:
```py
{'name': 'Mike Hawk'}
```
  
**OR** With `temp` method

`test.py`:
```py
from iniparser2 import INI_TEMP

x = INI_TEMP()
data = x.parse(
"""
name=Mike Hawk
""")

print(data)
```

#### Output:
```py
{'name': 'Mike Hawk'}
```

**OR** With section

`test.ini`:
```ini
[id]
name=Mike Hawk
age=-69
```

`test.py`:
```py
from iniparser2 import INI

x = INI('test.ini','id') # 'id' is the section name
data = x.get()

print(data)
```

#### Output:
```py
{'name': 'Mike Hawk', 'age': '-69'}
```

**pass_section** argument

`test.ini`:
```ini
brief=someone's identity

[id]
name=Mike Hawk
age=-69
```

`test.py`:
```py
from iniparser2 import INI

x = INI('test.ini',pass_section=True) # or you just don't have to put the section name, it will override the `pass_section` argument
data = x.get()

print(data)
```

#### Output:
```py
{'brief': "someone's identity", 'id': {'name': 'Mike Hawk', 'age': '-69'}}
```

**These example below is for properties stuff**
</br>
basic example

the `test.ini` file is empty

`test.py`:
```py
from iniparser2 import INI

x = INI('test.ini')
x.set('name','Mike Hawk')
```

and the `test.ini` file would be like this
```ini
name=Mike Hawk
```

it would update the value of the property if there's an existing property inside the file

to unset property
`test.py`:
```py
from iniparser2 import INI

x = INI('test.ini')
x.unset('name')
```

and the property would be gone!
