"""Colors enumeration definition"""

from bisect import bisect
from enum import Enum

import re

from archey.environment import Environment


# REGEXP compiled pattern matching ANSI/ECMA-48 color escape codes.
ANSI_ECMA_REGEXP = re.compile(r'\x1b\[\d+(?:(?:;\d+)+)?m')


class Colors(Enum):
    """
    ANSI terminal colors enumeration.
    Supports an arbitrary number of display attributes.

    See <http://www.termsys.demon.co.uk/vtansi.htm#colors>.
    """
    CLEAR = (0,)
    RED_NORMAL = (0, 31)
    RED_BRIGHT = (1, 31)
    GREEN_NORMAL = (0, 32)
    GREEN_BRIGHT = (1, 32)
    YELLOW_NORMAL = (0, 33)
    YELLOW_BRIGHT = (1, 33)
    BLUE_NORMAL = (0, 34)
    BLUE_BRIGHT = (1, 34)
    MAGENTA_NORMAL = (0, 35)
    MAGENTA_BRIGHT = (1, 35)
    CYAN_NORMAL = (0, 36)
    CYAN_BRIGHT = (1, 36)
    WHITE_NORMAL = (0, 37)
    WHITE_BRIGHT = (1, 37)

    def __str__(self):
        return self.escape_code_from_attrs(
            ';'.join(map(str, self.value))
        )

    @staticmethod
    def escape_code_from_attrs(display_attrs: str) -> str:
        """
        Build and return an ANSI/ECMA-48 escape code string from passed display attributes.
        """
        if Environment.NO_COLOR:
            return ''

        return f'\x1b[{display_attrs}m'

    @staticmethod
    def get_level_color(value: float, yellow_bpt: float, red_bpt: float) -> 'Colors':
        """Returns the best level color according to `value` compared to `{yellow,red}_bpt`"""
        level_colors = (Colors.GREEN_NORMAL, Colors.YELLOW_NORMAL, Colors.RED_NORMAL)

        return level_colors[bisect((yellow_bpt, red_bpt), value)]

    @staticmethod
    def remove_colors(string: str) -> str:
        """Simple DRY method to remove any ANSI/ECMA-48 color escape code from passed `string`"""
        return ANSI_ECMA_REGEXP.sub('', string)
