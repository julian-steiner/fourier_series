import numpy as np
import cv2.cv2 as cv
import random
from time import struct_time, time
from Vector import Vector
from math import e, floor, pi
from debugUtilities import prints
from integrate import integrate_fourier

class Screen:
    def __init__(self, shape):
        self.shape = shape
        self.window_p = np.zeros((shape[0], shape[1], 3)) # A screen for permanent stuff
        self.window_t = np.zeros((shape[0], shape[1], 3)) # A temporary screen for animated stuff
        self.canvas_number = random.random()
        self.vector_list = []
        self.position = [0, 0]
        self.axis_length = 3
        self.position_p = [0, 0]
        self.timelapse = 1
        self.opacity = 0.3
        self.flipped = False
        self.blank_lines = []

    def calculate_vectors(self, function, n_vectors):
        for i in range(1, n_vectors):
            position_c1 = integrate_fourier(function, 0.001, i)
            position_c2 = integrate_fourier(function, 0.001, -i)
            if not self.flipped:
                self.vector_list.append(Vector(position_c1, i))
                self.vector_list.append(Vector(position_c2, -i))
            else:
                self.vector_list.append(Vector(position_c1*-1, i))
                self.vector_list.append(Vector(position_c2*-1, -i))
        self.vector_list.sort(key=lambda x: x.length_r, reverse=True)
        
    def handle_vectors(self, t):
        position_c = [0, 0]
        for vector in self.vector_list:
            position_c = self.position[:]
            position_c[0] += np.real(vector.length * (e ** (vector.speed * 1j * t)))
            position_c[1] += np.imag(vector.length * (e ** (vector.speed * 1j * t))) 
            cv.line(self.window_t, self.translate_coords(self.position), self.translate_coords(position_c), (0, 0, self.opacity * 2.5))
            # if vector.speed != 0:
                # cv.circle(self.window_t, self.translate_coords(self.position), floor((vector.length_r * (self.shape[0] / self.axis_length)) / 2), [self.opacity, self.opacity, self.opacity])
            self.position = position_c
        position_translate = self.translate_coords(position_c)
        position_p_translate = self.translate_coords(self.position_p)
        try:
            blank = False
            for i in range(len(self.blank_lines)):
                if self.blank_lines[i][0] < (t % (2 * pi)) / (2 * pi) < self.blank_lines[i][1]:
                    blank = True
                    self.position_p = [0, 0]
                    break
            if self.position_p == [0, 0] or blank:
                print("Blank")
                pass
            else:
                cv.line(self.window_p, (position_p_translate[0], position_p_translate[1]), (position_translate[0], position_translate[1]), [255, 255, 255])
        except:
            pass
        self.position_p = position_c
        self.position = [0, 0]

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def translate_coords(self, coords):
        x = floor(self.translate(coords[0], -self.axis_length, self.axis_length, 0, self.shape[0]))
        y = floor(self.translate(coords[1], self.axis_length, -self.axis_length, 0, self.shape[1]))
        return x, y

    def update_screen(self):
        complete_window = np.add(self.window_p, self.window_t)
        if(self.flipped):
            complete_window = cv.flip(complete_window, 1)
        cv.imshow(str(self.canvas_number), complete_window)
        self.window_t = np.zeros((self.shape[0], self.shape[1], 3))

    def show(self):
        s_time = time()
        t = 0
        slow = False
        self.handle_vectors(0)
        self.update_screen()
        cv.waitKey(0)
        while True:
            t += 0.01 * self.timelapse
            self.handle_vectors(t)
            self.update_screen()
            k = cv.waitKey(1)
