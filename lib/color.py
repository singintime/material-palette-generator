from math import pow
from re import fullmatch


# Our eyes are very sensitive to green, moderately to red and not so much to blue.
# These coefficients are the W3C recommendation to compute relative color luminance.
# Please refer to https://www.w3.org/WAI/GL/wiki/Relative_luminance for further info.


LUMINANCE_R = 0.2126
LUMINANCE_G = 0.7152
LUMINANCE_B = 0.0722
LUMINANCE_THRESHOLD = 0.03928
LUMINANCE_DIVIDE = 12.92
LUMINANCE_BIAS = 0.055
LUMINANCE_GAMMA = 2.4

""" Clipping a value in the [min, max] range """


def clip(value, lower, upper):
    return min(max(value, lower), upper)


"""
Correct an RGB component for relative luminance calculation, according to W3C specs.
Please refer to https://www.w3.org/WAI/GL/wiki/Relative_luminance for further info.
"""


def correctForLuminance(value):
    if value <= LUMINANCE_THRESHOLD:
        return value / LUMINANCE_DIVIDE
    return pow((value + LUMINANCE_BIAS) / (1 + LUMINANCE_BIAS), LUMINANCE_GAMMA)


"""
Convert a normalized float ([0,1]) into an 8 bit hex string ([00,ff])
"""


def floatToHex(value):
    int_value = round(value * 255)
    return format(int_value, "02x")


"""
Convert a 8 bit hex string ([00,ff]) into a normalized float ([0,1])
"""


def hexToFloat(string):
    return int(string, 16) / 255


"""
Class representing an RGB color.
RGB components are stored as floating point values normalized and clipped
in the range [0,1]. This allows to simplify math operations on the values,
and to have much smaller rounding errors when performing them
with respect to the equivalent 8 bit integer representation ([0,255]).
"""


class Color:
    @staticmethod
    def fromHex(hex):
        if not fullmatch("^#[0-9A-Fa-f]{6}$", hex):
            return None
        return Color(hexToFloat(hex[1:3]), hexToFloat(hex[3:5]), hexToFloat(hex[5:7]))

    def __init__(self, r=0, g=0, b=0):
        self.r = r
        self.g = g
        self.b = b

    @property
    def r(self):
        return self.__r

    @r.setter
    def r(self, value):
        self.__r = clip(value, 0, 1)

    @property
    def g(self):
        return self.__g

    @g.setter
    def g(self, value):
        self.__g = clip(value, 0, 1)

    @property
    def b(self):
        return self.__b

    @b.setter
    def b(self, value):
        self.__b = clip(value, 0, 1)

    """
    Hex string representing the color in the RGB space
    """

    @property
    def hex(self):
        return f"#{floatToHex(self.r)}{floatToHex(self.g)}{floatToHex(self.b)}"

    """
    Keys and values of RGB components, ordered by magnitude
    """

    @property
    def ordered_components(self):
        comps = sorted(
            [("r", self.r), ("g", self.g), ("b", self.b)], key=lambda x: x[1]
        )
        return {"keys": [x[0] for x in comps], "values": [x[1] for x in comps]}

    """
    Color luminance - perceived brightness according to the sensitivity of the human eye.
    Best used to determine relative contrasts, i.e. how much a color is actually brighter
    or darker than another one.
    """

    @property
    def luminance(self):
        r = correctForLuminance(self.r)
        g = correctForLuminance(self.g)
        b = correctForLuminance(self.b)
        return LUMINANCE_R * r + LUMINANCE_G * g + LUMINANCE_B * b

    """
    Color lightness - average of brightest and darkest component.
    Best used to lighten or darken a color while preserving the hue.

    Lightness is adjusted by adding the same value to the brightest and darkest component,
    and computing the one in between to preserve the original relative ratios.
    """

    @property
    def lightness(self):
        l, _, h = sorted([self.r, self.g, self.b])
        return (l + h) / 2

    @lightness.setter
    def lightness(self, value):
        ordered = self.ordered_components
        keys = ordered["keys"]
        l, m, h = ordered["values"]

        b = 0 if l == h else (m - l) / (h - l)
        a = 1 - b

        diff = clip(value, 0, 1) - self.lightness
        new_l = l + diff
        new_h = h + diff

        if new_l < 0:
            new_h += new_l
            new_l = 0

        if new_h > 1:
            new_l += new_h - 1
            new_h = 1

        self.__setattr__(keys[0], new_l)
        self.__setattr__(keys[1], a * new_l + b * new_h)
        self.__setattr__(keys[2], new_h)

    """
    Moves the color towards black for negative amounts (-1 = full black),
    or towards white for positive amounts (1 = full white)
    """

    def scale(self, amount):
        clamped_amount = clip(amount, -1, 1)

        beta = abs(clamped_amount)
        alpha = 1 - beta

        shade = (0 if clamped_amount < 0 else 1) * beta

        self.r = self.r * alpha + shade
        self.g = self.g * alpha + shade
        self.b = self.b * alpha + shade

    """
    Maximise the saturation of the color's hue by setting
    the darkest component to 0, the brightest component to 1,
    and computing the one in between to preserve the original relative ratios.
    """

    def saturate(self):
        ordered = self.ordered_components
        keys = ordered["keys"]
        l, m, h = ordered["values"]

        self.__setattr__(keys[0], 0.5 if l == h else 0)
        self.__setattr__(keys[1], 0.5 if l == h else (m - l) / (h - l))
        self.__setattr__(keys[2], 0.5 if l == h else 1)

    """
    Create a new color instance with the same RGB values as the source one.
    """

    def clone(self):
        return Color(self.r, self.g, self.b)
