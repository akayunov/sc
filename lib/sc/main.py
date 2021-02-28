import numpy as np
import cv2
from pathlib import Path
from .parsers.resourceparser import ResourceParser
from .parsers.minimapparser import MiniMapParser
from .const import MainWindow, RESOURCE_DIR, FONT
from .videoreader import VideoReader
from .temp_matcher import TempMatcher

HP_LINE_TEMPL = cv2.imread(str(Path(RESOURCE_DIR, 'hp-line.png')), 0)
_, HP_LINE_TEMPL_MASK = cv2.threshold(
    cv2.imread(str(Path(RESOURCE_DIR, 'hp-line-mask.png')), 0),
    127,
    1,
    cv2.THRESH_BINARY)


def run():
    resource_paser = ResourceParser()
    mini_map_parser = MiniMapParser()
    video_reader = VideoReader(str(Path(RESOURCE_DIR, 'video.mp4')))

    key_code = None
    while True:
        i, frame = video_reader.next()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # match template
        asd=  HP_LINE_TEMPL
        qwe = HP_LINE_TEMPL_MASK
        loc = TempMatcher.match(HP_LINE_TEMPL, frame_gray, threshold=0.6, mask=HP_LINE_TEMPL_MASK)
        w, h = HP_LINE_TEMPL.shape[::-1]
        for pt in zip(*loc[::-1]):
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imshow(MainWindow.name, frame)
        # parse resources
        minerals, gas, supply_exists, supply_avail = resource_paser.parse(frame)
        # mini_map_parser.parse(frame)
        cv2.putText(frame, f'{minerals}', (resource_paser.y, resource_paser.x + 40), FONT, 1, (0, 0, 255), 2,
                    cv2.LINE_AA)
        # cv2.putText(frame, f'Frame number: {i} key_code:{key_code} {minerals}-{gas}-{supply_exists}-{supply_avail}', (10, 55),
        #             FONT, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow(MainWindow.name, frame)

        key_code = cv2.waitKey(0)
        if key_code == 27:
            break
        elif key_code == 32:
            video_reader.next(1000)

    video_reader.close()
