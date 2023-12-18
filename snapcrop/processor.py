import cv2
import math
from scipy import ndimage
import numpy as np

class Closer:
    def __init__(self, kernel_size = 3, iterations = 10, output_process = False):
        self._kernel_size = kernel_size
        self._iterations = iterations
        self.output_process = output_process


    def __call__(self, image):
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, 
            (self._kernel_size, self._kernel_size)
        )
        closed = cv2.morphologyEx(
            image, 
            cv2.MORPH_CLOSE, 
            kernel,
            iterations = self._iterations
        )

        if self.output_process: cv2.imwrite('output/closed.jpg', closed)
        return closed


class Opener:
    def __init__(self, kernel_size = 3, iterations = 25, output_process = False):
        self._kernel_size = kernel_size
        self._iterations = iterations
        self.output_process = output_process


    def __call__(self, image):
        kernel = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, 
            (self._kernel_size, self._kernel_size)
        )
        opened = cv2.morphologyEx(
            image, 
            cv2.MORPH_OPEN,
            kernel,
            iterations = self._iterations 
        )

        if self.output_process: cv2.imwrite('output/opened.jpg', opened)
        return opened


class EdgeDetector:
    def __init__(self, output_process = False):
        self.output_process = output_process


    def __call__(self, image, thresh1 = 50, thresh2 = 150, apertureSize = 3):
        edges = cv2.Canny(image, thresh1, thresh2, apertureSize = apertureSize)
        if self.output_process: cv2.imwrite('output/edges.jpg', edges)
        return edges