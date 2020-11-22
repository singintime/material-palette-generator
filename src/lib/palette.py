from .color import Color
from math import log2

black = "#000000"
white = "#ffffff"

"""
Generates a Material palette from a hex code
"""


def generatePalette(hex):
    color = Color.fromHex(hex)

    if not color:
        return None

    gamma = -log2(color.lightness)

    result = {"contrast": dict()}
    for i in range(1, 10):
        name = f"{i * 100}"
        shade = color.clone()
        shade.lightness = (1 - i / 10) ** gamma
        result[name] = shade.hex
        result["contrast"][name] = black if shade.luminance > 0.5 else white

    color.saturate()
    for i in [1, 2, 4, 7]:
        name = f"A{i * 100}"
        shade = color.clone()
        shade.lightness = 1 - i / 10
        print(shade.lightness)
        result[name] = shade.hex
        result["contrast"][name] = black if shade.luminance > 0.5 else white

    return result
