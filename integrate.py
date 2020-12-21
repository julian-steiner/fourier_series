from math import floor, e, pi
import numpy as np

def integrate_fourier(function, dt, n):
    sum = 0
    t = 0 
    for i in range(floor(1 / dt)):
        sum += function(t) * (e ** (-n * 2 * pi * 1j * t)) * dt
        t += dt
    return sum



