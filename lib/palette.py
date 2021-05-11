from lib.color import Color

black = "#000000"
white = "#ffffff"

"""
Generates a Material palette from a hex code
"""


def generatePalette(hex):
    color = Color.fromHex(hex)

    if not color:
        return None

    result = {}
    contrast = {}

    for i in [0.5, *range(1, 10)]:
        name = f"{int(i * 100)}"
        shade = color.clone()
        shade.scale((5 - i) / 5)
        result[name] = shade.hex
        contrast[name] = black if shade.luminance > 0.5 else white

    color.saturate()
    for i in [1, 2, 4, 7]:
        name = f"A{i * 100}"
        shade = color.clone()
        shade.scale((5 - i) / 5)
        result[name] = shade.hex
        contrast[name] = black if shade.luminance > 0.5 else white

    result["contrast"] = contrast

    return result
