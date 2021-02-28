import math

import numpy as np
import cv2
from pathlib import Path

from sc.main import HP_LINE_TEMPL
from sc.temp_matcher import TempMatcher


def run():
    frame = cv2.imread('probes.jpg')
    # frame = cv2.GaussianBlur(frame,(7,7),0)
    # frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # dst = cv2.Canny(frame, 50, 200, None, 3)

    # cv2.imwrite((str(Path(RESOURCE_DIR, 'hp-line-contur.bmp'))),dst)
    loc = TempMatcher.match(HP_LINE_TEMPL, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), threshold=0.5)
    w, h = HP_LINE_TEMPL.shape[::-1]
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    # lines = cv2.HoughLinesP(dst, 1, math.pi / 2, 2, None, 40, 4)
    # print(lines)
    # for ll in lines:
    #     for line in ll:
    #         pt1 = (line[0], line[1])
    #         pt2 = (line[2], line[3])
    #         cv2.line(frame, pt1, pt2, (0, 0, 255), 3)
    # cv2.imshow(f'{DebugWindow.name}-lines', frame)
    # # cv2.imshow(f'{DebugWindow.name}-blue', frame[:, :,0])
    # cv2.imshow(f'{DebugWindow.name}-green', frame[:, :, 1])
    # cv2.imshow(f'{DebugWindow.name}-red', frame[:, :, 2])
    cv2.imshow('main', frame)
    # cv2.imshow('debug', dst)
    key_code = cv2.waitKey(0)
    if key_code == 27:
        return
    elif key_code == 32:
        return


run()
