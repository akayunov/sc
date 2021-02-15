from pathlib import Path
import numpy
import cv2
from ..const import DebugWindow, RESOURCE_DIR, FONT
from ..temp_matcher import TempMatcher


def parse_green_color(roi):
    lower_val = numpy.array([170, 170, 170])
    upper_val = numpy.array([190, 190, 190])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(roi, lower_val, upper_val)

    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    only_green = cv2.bitwise_and(gray, gray, mask=mask)

    return only_green


class MiniMapParser:
    x = 547
    x_shift = 153
    y = 19
    y_shift = 175

    def __init__(self):
        pass

    def parse(self, frame):
        cv2.imshow(DebugWindow.name, cv2.resize(frame[self.x:self.x + self.x_shift, self.y:self.y + self.y_shift], None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                                                interpolation=cv2.INTER_CUBIC))
        print(frame[40, 684])
        cv2.waitKey(0)
        roi_gray = parse_green_color(frame[self.x:self.x + self.x_shift, self.y:self.y + self.y_shift])
        cv2.imshow(DebugWindow.name, cv2.resize(roi_gray, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                                                interpolation=cv2.INTER_CUBIC))
