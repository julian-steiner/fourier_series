import numpy as np
def bezier(start, control1, control2, end, t, tmax):
    x = (((tmax - t)**3 * start[0]) + 3 * (tmax - t)**2 * t * control1[0] + 3 * (tmax - t)* t**2 * control2[0] + t**3 * end[0]) * tmax ** -3
    y = (((tmax - t)**3 * start[1]) + 3 * (tmax - t)**2 * t * control1[1] + 3 * (tmax - t)* t**2 * control2[1] + t**3 * end[1]) * tmax ** -3
    return x + (y * 1j)

def CubicBezier(start, control1, control2, end, t, tmax):
    x = (((tmax - t)**3 * np.real(start)) + 3 * (tmax - t)**2 * t * np.real(control1) + 3 * (tmax - t)* t**2 * np.real(control2) + t**3 * np.real(end)) * tmax ** -3 
    y = (((tmax - t)**3 * np.imag(start)) + 3 * (tmax - t)**2 * t * np.imag(control1) + 3 * (tmax - t)* t**2 * np.imag(control2) + t**3 * np.imag(end)) * tmax ** -3
    return x + (y * 1j)

def Line(start, end, t, tmax):
    x = np.real(start) + (np.real(end) - np.real(start)) * t / tmax
    y = np.imag(start) + (np.imag(end) - np.imag(start)) * t / tmax
    return x + (y * 1j)

def quadratic(p1, p2, p3, t, tmax):
    x = ((tmax - t)**2 * p1[0] + 2 * (tmax - t)* t * p2[0] + t**2 * p3[0]) * tmax ** -2
    y = ((tmax - t)**2 * p1[1] + 2 * (tmax - t)* t * p2[1] + t**2 * p3[1]) * tmax ** -2
    return x + (y * 1j)

class curveFromSvg:
    def __init__(self, curves):
        self.empty_lines = []
        self.curves = []
        self.totalCurves = 0
        if(len(curves) > 1):
            for i in range(len(curves)):
                for curve in curves[i]:
                    self.curves.append(curve)
        else:
            self.curves = self.optimizeCurve(curves[0])
            self.totalCurves = len(self.curves)

        self.curves = self.optimizeCurve(self.curves)
        self.totalCurves = len(self.curves)
        self.optimizeBlanks()

        print(len(self.curves))
        print(len(self.curves[0]))


        # for i in range(1, len(self.curves)):
        #     if self.curves[i - 1][-1] != self.curves[i][0]:
        #         self.empty_lines.append([(i-1) / self.totalCurves, i / self.totalCurves])
        #         self.totalCurves += 1
        #         print(self.curves[i-1][-1])
        #         self.curves.insert(i, [self.curves[i-1][-1], self.curves[i][0]])
        # if self.curves[-1][-1] != self.curves[0][0]:
        #     curves_t = self.curves[:]
        #     self.totalCurves += 1
        #     self.empty_lines.append([1 - (1 / self.totalCurves), 1])
        #     curves_t.append([self.curves[-1][-1], self.curves[0][0]])
        #     self.curves = curves_t

    def optimizeCurve(self, curve):
        for i in range(1, len(curve)):
            if curve[i - 1][-1] != curve[i][0]:
                self.empty_lines.append([i + self.totalCurves, i+1 + self.totalCurves])
                self.totalCurves += 1
                print(curve[i-1][-1])
                curve.insert(i, [curve[i-1][-1], curve[i][0]])
        if curve[-1][-1] != curve[0][0]:
            curves_t = curve[:]
            self.totalCurves += 1
            self.empty_lines.append([len(curve) + self.totalCurves, len(curve)+1 + self.totalCurves])
            curves_t.append([curve[-1][-1], curve[0][0]])
            curve = curves_t
        return curve

    def optimizeBlanks(self):
        for i in range(len(self.empty_lines)):
            self.empty_lines[i][0] /= self.totalCurves
            self.empty_lines[i][1] /= self.totalCurves

    def getBlank(self):
        return self.empty_lines

    def getValue(self, t):
        for i in range(len(self.curves)):
            if t <= ((i + 1) / len(self.curves)):
                if len(self.curves[i]) == 4:
                    return CubicBezier(self.curves[i][0], self.curves[i][1], self.curves[i][2], self.curves[i][3], t - (i) * (1/len(self.curves)), 1 / len(self.curves))
                elif len(self.curves[i]) == 2:
                    return Line(self.curves[i][0], self.curves[i][1], t - (i) * (1/len(self.curves)), 1 / len(self.curves))

class chainedCubicBezier:
    def __init__(self, curves_list):
        self.curves_list = curves_list
    def getValue(self, t):
        for i in range(len(self.curves_list)):
            if t <= ((i + 1) / len(self.curves_list)):
                return bezier(self.curves_list[i][0], self.curves_list[i][1], self.curves_list[i][2], self.curves_list[i][3], t - (i) * (1/len(self.curves_list)), 1 / len(self.curves_list))

class chainedBezier:
    def __init__(self, curves_list):
        self.curves_list = curves_list
    def getValue(self, t):
        for i in range(len(self.curves_list)):
            if t <= ((i + 1) / len(self.curves_list)):
                return quadratic(self.curves_list[i][0], self.curves_list[i][1], self.curves_list[i][2], t - (i) * (1/len(self.curves_list)), 1 / len(self.curves_list))
