import math
from dataclasses import dataclass
from pathlib import Path
import numpy
import cv2
from ..const import DebugWindow, RESOURCE_DIR, FONT, ScreenSize , MiniMapSize
from ..temp_matcher import TempMatcher


@dataclass
class B:
    l: int = 0
    h: int = 255


class Green:
    b = B(l=0, h=50)
    g = B(l=60, h=255)
    r = B(l=0, h=50)


class Red:
    b = B(l=0, h=50)
    g = B(l=0, h=50)
    r = B(l=60, h=255)


class White:
    b = B(l=170, h=255)
    g = B(l=170, h=255)
    r = B(l=170, h=255)


WHITE = White()
GREEN = Green()
RED = Red()


# b,g, r
def parse_color(roi, color):
    lower_val = numpy.array([color.b.l, color.g.l, color.r.l])
    upper_val = numpy.array([color.b.h, color.g.h, color.r.h])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(roi, lower_val, upper_val)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    only_green = cv2.bitwise_and(gray, gray, mask=mask)
    ret_, only_green = cv2.threshold(only_green, 0, 255, cv2.THRESH_BINARY)
    return only_green


minimap = cv2.imread(str(Path(RESOURCE_DIR, 'minimap1.bmp')))


class MiniMapParser:
    m = MiniMapSize

    def __init__(self):
        pass

    def parse(self, frame):
        cv2.imshow(DebugWindow.name, cv2.resize(frame[self.m.x:self.m.x + self.m.x_shift, self.m.y:self.m.y + self.m.y_shift], None,
                                                fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                                                interpolation=cv2.INTER_CUBIC))
        # cv2.imwrite((str(Path(RESOURCE_DIR, 'hp-line-contur.bmp'))), frame[self.x:self.x + self.x_shift, self.y:self.y + self.y_shift])
        cv2.waitKey(0)

        roi_green = parse_color(frame[self.m.x:self.m.x + self.m.x_shift, self.m.y:self.m.y + self.m.y_shift], color=GREEN)
        green_contours, hierarchy = cv2.findContours(roi_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(roi_green, green_contours, -1, (0, 255, 0), 3)
        # cv2.imshow(DebugWindow.name, cv2.resize(roi_green, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
        #                                         interpolation=cv2.INTER_CUBIC))
        # cv2.waitKey(0)
        roi_red = parse_color(frame[self.m.x:self.m.x + self.m.x_shift, self.m.y:self.m.y + self.m.y_shift], color=RED)
        red_contours, hierarchy = cv2.findContours(roi_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # cv2.drawContours(roi_red, red_contours, -1, (0, 255, 0), 3)
        # cv2.imshow(DebugWindow.name, cv2.resize(roi_red, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
        #                                         interpolation=cv2.INTER_CUBIC))
        # cv2.waitKey(0)
        roi = frame[self.m.x:self.m.x + self.m.x_shift, self.m.y:self.m.y + self.m.y_shift]
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        dst = cv2.Canny(gray, 50, 200, None, 3)

        # Copy edges to the images that will display the results in BGR
        cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

        lines = cv2.HoughLines(dst, 1, numpy.pi / 180, 150, None, 0, 0)

        print(lines)
        if lines is not None:

            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
                pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
                cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
        cv2.imshow(DebugWindow.name, cv2.resize(cdst, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                                                interpolation=cv2.INTER_CUBIC))
        cv2.waitKey(0)