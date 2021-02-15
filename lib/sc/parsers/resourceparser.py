from pathlib import Path
import numpy
import cv2
from ..const import DebugWindow, RESOURCE_DIR
from ..temp_matcher import TempMatcher


def parse_while_color(roi):
    # set lower and upper color limits
    lower_val = numpy.array([180, 180, 180])
    upper_val = numpy.array([255, 255, 255])
    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(roi, lower_val, upper_val)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    return cv2.bitwise_and(gray, gray, mask=mask)


class ResourceParser:
    x = 14
    x_shift = 9
    y = 1016
    y_shift = 62

    DIGIT_TEMPLS = {0: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-0.png')))),
                    1: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-1.png')))),
                    2: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-2.png')))),
                    3: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-3.png')))),
                    4: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-4.png')))),
                    5: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-5.png')))),
                    6: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-6.png')))),
                    7: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-7.png')))),
                    8: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-8.png')))),
                    9: parse_while_color(cv2.imread(str(Path(RESOURCE_DIR, 'digital-9.png'))))}

    cv2.imwrite(str(Path(RESOURCE_DIR, 'res.bmp')), DIGIT_TEMPLS[3])

    def __init__(self):
        pass

    def parse(self, frame):
        roi_gray = parse_while_color(frame[self.x:self.x + self.x_shift, self.y:self.y + self.y_shift])
        cv2.imshow(DebugWindow.name, cv2.resize(roi_gray, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                                                interpolation=cv2.INTER_CUBIC))
        cv2.waitKey(0)
        # debug = numpy.copy(roi_gray)
        values = []
        result = ''
        for _ in range(5):
            max_value = 0
            coord = (0, 0)
            number = 0
            for templ_name, templ_value in self.DIGIT_TEMPLS.items():
                # if ROI.shape[0] != templ['value'].shape[0]:
                #     cv2.imshow(DebugWindow.name, ROI)
                #     cv2.imwrite(str(Path(RESOURCE_DIR, 'res.bmp')), ROI)
                #     raise Exception(
                #         f'Size of templ {templ["name"]}:{templ["value"].shape[0]}  and ROI: {ROI.shape[0]} are different')
                loc, max_ = TempMatcher.find_max_match(templ_value, roi_gray)
                if max_ > max_value:
                    max_value = max_
                    coord = loc
                    number = templ_name

            if max_value > 0.5:
                values.append((str(number), coord))
                w, h = templ_value.shape[::-1]
                roi_gray[coord[1]:, coord[0]: 1 + coord[0] + h] = 0
                # debug = numpy.concatenate(debug, roi_gray)
                cv2.imshow(DebugWindow.name, cv2.resize(roi_gray, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                                                        interpolation=cv2.INTER_CUBIC))
                cv2.waitKey(0)
        # cv2.imshow(DebugWindow.name, cv2.resize(debug, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
        #                                         interpolation=cv2.INTER_CUBIC))
        values = sorted(values, key=lambda x: x[1][0])
        result = ''.join(map(lambda x: x[0], values))
        return result, 0, 0, 0
