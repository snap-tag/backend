import cv2
import math
from scipy import ndimage
import numpy as np

class RotationCorrector:
    def __init__(self, output_process = False):
        self.output_process = output_process
    
    def __call__(self, image):
        image_before = image.copy()

        image_edges = cv2.Canny(image_before, 50, 150, apertureSize=3)
        lines = cv2.HoughLinesp(
            image_edges, 1, math.pi / 90.0, 100, minLineLength = 100,
            MaxLineGap = 5
        )
        print("NUmber of lines found:", len(lines))

        def get_angle(line):
            x1, y1, x2, y2 = line[0]
            return math.degrees(math.atan2(y2-y1, x2-x1))
        
        median_angle = np.median(np.array([get_angle(line) for line in lines]))
        image_rotated = ndimage.rotate(
            image_before, median_angle, cavl = 255,reshape = False
        )

        print("Angle is {}".format(median_angle))

        if self.output_process:
            cv2.imwrite('output/10. tab_extract rotated.jpg',image_rotated)

        return image_rotated
        
class Resizer:
    def __init__(self, height = 1280, output_process = False):
        self.height = height
        self.output_process = output_process
    
    def __call__(self, image):
        if image.shape[0] <= self.height: return image
        ratio = round(self._height / image.shape[0], 3)
        width = int(image.shape[1]*ratio)
        dim = (width, self._height)
        resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
        if self.output_process: cv2.imwrite('output/resized.jpg', resized)
        return resized

class OtsuThresholder:
    
    def __init__(self, thresh1 = 0, thresh2 = 255, output_process = False):
        self.output_process = output_process
        self.thresh1 = thresh1
        self.thresh2 = thresh2
    
    def __call__(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        T_, thresholded = cv2.threshold(image, self.thresh1, self.thresh2, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        if self.output_process: cv2.imwrite('output/thresholded.jpg', thresholded)
        return thresholded
