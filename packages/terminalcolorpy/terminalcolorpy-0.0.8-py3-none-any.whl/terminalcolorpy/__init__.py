__version__ = '0.0.8'

import typing
import secrets

"""
2021-2021 AmmarSys

Open Sourse License: Apache 2.0

Built with: Python 3

Long description: This is a simple package to print colored messages using ASCI to the terminal built with python 3.
Short description: A module to markup terminal text
"""


class colors:
    highlight_dicts = {
        'gray': '\x1b[7m',
        'pink': '\x1b[45m',
        'black': '\x1b[40m',
        'yellow': '\x1b[43m',
        'green': '\x1b[42m',
        'blue': '\x1b[44m',
        'red': '\x1b[41m'
    }

    color_dict = {
        'pink': '\033[95m',
        'blue': '\033[94m',
        'cyan': '\033[96m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'black': '\x1b[30m',
        'orange': '\033[38;2;255;69;0m'
    }

    text_markup_dict = {
        'bold': '\033[1m',
        'underline': '\033[4m',
        'italic': '\x1B[3m',
        'striked': ''
    }


clr = ['\033[91m', '\033[38;2;255;69;0m', '\033[93m', '\033[92m', '\033[94m']
end = '\033[0m'

def prainbow(text: str):
    return ''.join([secrets.choice(clr) + i for i in text]) + end


def hex_to_rgb(hexcode):
    hexcode = hexcode.lstrip('#')
    hlen = len(hexcode)
    return list(int(hexcode[i:i + hlen // 3], 16) for i in range(0, hlen, hlen // 3))


def rgb_to_ansii(rgb: list, text: str) -> str:
    return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{text}"


def pcolor(text: str,
           color: typing.Union[list, str],
           highlight: typing.Union[list, str] = None,
           markup: list = None,
           ) -> str:
    try:
        highlightMaybe = ''
        expression = ''
        if type(highlight) == str:
            if highlight in colors.highlight_dicts:
                highlightMaybe = colors.highlight_dicts[highlight]
            else:
                rgbval = hex_to_rgb(highlight)
                highlightMaybe = f"\033[48;2;{rgbval[0]};{rgbval[1]};{rgbval[2]}m"

        if type(highlight) == list:
            highlightMaybe = f'\033[48;2;{highlight[0]};{highlight[1]};{highlight[2]}m'

        if type(color) == list:
            if any(i > 255 or i < 0 for i in color):
                raise KeyError
            expression = rgb_to_ansii(color, text) + end

        if type(color) == str:
            torgb = hex_to_rgb(color)
            expression = rgb_to_ansii(torgb, text) + end

        if markup is None:
            if highlight is None:
                return expression
            else:
                return highlightMaybe + expression

        if markup is not None:
            expression_markup = "".join([colors.text_markup_dict[i] for i in markup]) + expression
            if 'striked' not in markup:
                if highlight is None:
                    return expression_markup
                else:
                    return highlightMaybe + expression_markup
            else:
                no_color = text.split(expression_markup)
                no_text = expression_markup.split(text)
                striked_no_color = "".join([u'\u0336{}'.format(i) for i in no_color[0]]) + '\u0336'

                if highlight is None:
                    return no_text[0] + striked_no_color + no_text[1]
                else:
                    return highlightMaybe + no_text[0] + striked_no_color + no_text[1]
        else:
            raise KeyError

    except (KeyError, ValueError, IndexError):
        raise KeyError('You\'re proving a invalid argument, please look at the acceptable options at '
                       'https://www.github.com/ammar-sys/terminalcolorpy')


pc, pr = pcolor, prainbow
