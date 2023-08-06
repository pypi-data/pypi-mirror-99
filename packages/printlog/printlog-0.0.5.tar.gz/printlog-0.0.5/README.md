# Printlog

> Colorize your logs to spot them at a glance.

[![Latest Version on PyPI](https://img.shields.io/pypi/v/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)
[![Supported Implementations](https://img.shields.io/pypi/pyversions/pypi-template.svg)](https://pypi.python.org/pypi/pypi-template/)


## Install
````
pip install printlog
````

## Usage 

### Log
The methods in log automatically print.
```python
from printlog import log

log.success("It is a success")
log.success("It is a success with background", bg=True)
log.error("Is is an error")
log.error("Is is an error with background", bg=True)
```
*Result :*  
<center>
<img src="https://github.com/LudovicPatho/printlog/raw/main/img/example1.PNG" alt='example1'>
</center>

## Color
```python

from printlog.color import red, green, yellow, magenta, cyan 

print(red("This a red text"))
print(red("This a red text with background", bg=True))

print(green("This a green text"))
print(green("This a green text with background", bg=True))

print(yellow("This a yellow text"))
print(yellow("This a yellow text with background", bg=True))

print(blue("This a blue text"))
print(blue("This a blue text with background", bg=True))

print(magenta("This a magenta text"))
print(magenta("This a magenta text with background", bg=True))


print(cyan("This a cyan text"))
print(cyan("This a cyan text with background", bg=True))
```
*Result :*  
<center>
<img src="https://github.com/LudovicPatho/printlog/raw/main/img/example2.PNG" alt='example2'>
</center>