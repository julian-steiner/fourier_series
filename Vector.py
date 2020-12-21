from math import atan
import numpy as np

class Vector:
    def __init__(self, length, speed):
        self.length = length
        self.length_r = (np.real(length) ** 2 + np.imag(length)** 2) ** 0.5
        self.speed = speed