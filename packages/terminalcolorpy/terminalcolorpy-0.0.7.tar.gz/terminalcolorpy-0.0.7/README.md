# terminalcolorpy

![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

This is a simple package to print colored messages using ASCI to the terminal built with python 3.

# Usage of terminalcolorpy


Usage of it is pretty straight-forward,
```py
from terminalcolorpy import pcolor, prainbow

print(pc('Hello', color='#42f5d7',
         markup=['striked', 'bold', 'underline', 'italic'],
         highlight='#a8328b')
      )
```

TerminalColorPy has 2 main functions, 
- prainbow
- pcolor

**prainbow** It's alias is *pr*, takes a single parameter which is text to return as rainbow.

**pcolor** It's alias is *pc*, takes 4 parameteres, which are:
 - text (mandatory)
 - color (mandatory)
 - highlight 
 - markup

HighLight & Color take either a string, an RGB value or even a hex code. For example,
    
```python
from terminalcolorpy import pcolor

print(pcolor('Hello', color='#42f5d7',
         markup=['striked', 'bold', 'underline', 'italic'],
         highlight='#42f5d7')
      )

print(pcolor('World', color='red',
         markup=['striked', 'bold'],
         highlight='blue')
      )

print(pcolor('World', color=[122, 99, 0],
         markup=['bold'],
         highlight=[122, 100, 78])
      )
```

# List of accepted values
```python

    highlight_values = [
        'gray',
        'pink',
        'black',
        'yellow',
        'green',
        'blue',
        'red'
    ]

    color_values = [
        'pink',
        'blue',
        'cyan',
        'green',
        'yellow',
        'red',
        'black',
        'orange'
    ]

    text_markup_values = [
        'bold',
        'underline',
        'italic',
        'striked'
    ]
```

**Hex Generator** https://www.google.com/search?q=hex+color

**RGB Generator** https://www.w3schools.com/colors/colors_rgb.asp

It works on any terminals that support ASCII codes, include but not limited to:

| Terminals      | Works On |
| ----------- | ----------- |
| PyCharm      | True       |
| Python IDLE   | False        |
| Windows CMD    | False  |
| MacOS iTerm2         | True |
| VSCode | True
|  Visual Studio Code | True

*i haven't really used anything else, this list is to expand*