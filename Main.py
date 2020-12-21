import svgpathtools
from bezier import bezier, chainedBezier, chainedCubicBezier, curveFromSvg
from DrawingScreen import Screen
from math import *
from svgpathtools import *

fourierscreen = Screen([1080, 1080])

fourierscreen.axis_length = 10000

def adobeLogo(x):
    curves = []
    curves.append([(10, 10), (-50, 70), (30, 100), (-20, 0)])
    curves.append([(-20, 0), (-70, -100), (-100, -30), (0, -10)])
    curves.append([(0, -10), (100, 10), (70, -50), (10, 10)])
    curve = chainedCubicBezier(curves)
    return curve.getValue(x)

def nikeLogo(x):
    if x < 0.25:
        return bezier((9, 8), (0, 2), (-4, 0), (-6, 0), x, 0.25)
    elif x < 0.5:
        return bezier((-6, 0), (-9, 0), (-10, 3), (-6, 7), x - (0.25), 0.25)
    elif x < 0.75:
        return bezier((-6, 7), (-7, 4), (-6, 3), (-5, 3), x - (0.5), 0.25)
    else:
        return bezier((-5, 3), (-3, 3), (0, 4), (9, 8), x - (0.75), 0.25)

def macDonalds(x):
    curves = []
    curves.append([(0, 0), (1, 17), (7, 17), (9, 9)])
    curves.append([(9, 9), (12, 17), (17, 17), (18, 0)])
    curves.append([(18, 0), (18, 0), (16, 0), (16, 0)])
    curves.append([(16,0), (16, 16), (12, 16), (10, 2)])
    curves.append([(10, 2), (10, 2), (8, 2), (8, 2)])
    curves.append([(8, 2), (7, 16), (2, 16), (2, 0)])
    curves.append([(2, 0), (2, 0), (0, 0), (0, 0)])
    curve = chainedCubicBezier(curves)
    return curve.getValue(x)

# ## Axis length of 400
# fourierscreen.flipped = True
# paths, attributes = svg2paths('Pi-symbol.svg')
# curve = curveFromSvg(paths)
# def pi_curve(x):
#     global curve
#     return curve.getValue(x)
# fourierscreen.calculate_vectors(pi_curve, 200)

# Axis lenth of 70
# fourierscreen.flipped = True
# paths, attributes = svg2paths('note.svg')
# curve = curveFromSvg(paths)
# def violin_curve(x):
#     global curve
#     return curve.getValue(x)
# fourierscreen.calculate_vectors(violin_curve, 50)

# Axis lenth of 100
fourierscreen.flipped = True
paths, attributes = svg2paths('39881.svg')
curve = curveFromSvg(paths)
def violin_curve(x):
    global curve
    return curve.getValue(x)
fourierscreen.calculate_vectors(violin_curve, 200)

# # Axis lenth of 100
# paths, attributes = svg2paths('2.svg')
# curve = curveFromSvg(paths)
# def letter_2_curve(x):
#     global curve
#     return curve.getValue(x)
# fourierscreen.calculate_vectors(letter_2_curve, 300)
    
# Axis lenth of 100
# paths, attributes = svg2paths('google.svg')
# curve = curveFromSvg(paths)
# def letter_F_curve(x):
#     global curve
#     return curve.getValue(x)
# fourierscreen.calculate_vectors(letter_F_curve, 200)
    
fourierscreen.timelapse = 0.5
# print(curve.curves)
# print(curve.getBlank())

fourierscreen.blank_lines = curve.getBlank()

fourierscreen.show()
