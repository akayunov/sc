import cv2
import numpy as np


class TempMatcher:
    @classmethod
    def match(cls, template, roi, threshold=0.9):
        w, h = template.shape[::-1]
        frame_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(roi, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        return loc

    @classmethod
    def find_max_match(cls, template, roi_gray):

        res = cv2.matchTemplate(roi_gray, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= res.max())
        # for pt in zip(*loc[::-1]):
        #     cv2.rectangle(roi, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        ll = list(zip(*loc[::-1]))
        if ll:
            return ll[0], res.max()
