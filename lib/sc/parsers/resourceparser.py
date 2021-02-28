from pathlib import Path
import numpy
import cv2
from ..const import DebugWindow, RESOURCE_DIR, FONT
from ..temp_matcher import TempMatcher


def parse_while_color(roi):
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    ret_, img = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    return img


class ResourceParser:
    x = 15
    x_shift = 7
    y = 1010
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

    def __init__(self):
        pass

    def parse(self, frame):
        roi_gray = parse_while_color(frame[self.x:self.x + self.x_shift, self.y:self.y + self.y_shift])
        # cv2.imshow(DebugWindow.name, cv2.resize(roi_gray, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
        #                                         interpolation=cv2.INTER_CUBIC))
        # cv2.imwrite(str(Path(RESOURCE_DIR, 'hp-line-contur.bmp')), roi_gray)
        # cv2.waitKey(0)
        values = []
        for _ in range(5):
            max_value = 0
            coord = (0, 0)
            number = 0
            for templ_name, templ_value in self.DIGIT_TEMPLS.items():
                # if ROI.shape[0] != templ['value'].shape[0]:
                #     cv2.imshow(DebugWindow.name, ROI)
                #     cv2.imwrite(str(Path(RESOURCE_DIR, 'hp-line-contur.bmp')), ROI)
                #     raise Exception(
                #         f'Size of templ {templ["name"]}:{templ["value"].shape[0]}  and ROI: {ROI.shape[0]} are different')
                loc, max_ = TempMatcher.find_max_match(templ_value, roi_gray)
                print(templ_name, max_)
                if max_ > max_value:
                    max_value = max_
                    coord = loc
                    number = templ_name

            if max_value > 0.5:
                values.append((str(number), coord))
                h, w = self.DIGIT_TEMPLS[number].shape
                # roi_gray[coord[1], coord[0]] = 150
                # cv2.imshow(DebugWindow.name, cv2.resize(roi_gray, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                #                                         interpolation=cv2.INTER_CUBIC))
                # cv2.waitKey(0)
                roi_gray[coord[1]:, coord[0]: coord[0] + w] = 0

                # cv2.imshow(DebugWindow.name, cv2.resize(roi_gray, None, fx=DebugWindow.scale_x, fy=DebugWindow.scale_y,
                #                                         interpolation=cv2.INTER_CUBIC))

        values = sorted(values, key=lambda x: x[1][0])
        result = ''.join(map(lambda x: x[0], values))
        print(result)
        return result, 0, 0, 0
