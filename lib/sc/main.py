import numpy as np
import cv2
from pathlib import Path
from .parsers.resourceparser import ResourceParser
from .const import MainWindow, RESOURCE_DIR, FONT
from .videoreader import VideoReader
from .temp_matcher import TempMatcher

HP_LINE_TEMPL = cv2.imread(str(Path(RESOURCE_DIR, 'hp-line.png')), 0)


def run():
    resource_paser = ResourceParser()
    video_reader = VideoReader(str(Path(RESOURCE_DIR, 'video.mp4')))

    key_code = None
    while True:
        i, frame = video_reader.next()

        # match template
        TempMatcher.match(HP_LINE_TEMPL, frame)

        # parse resources
        minerals, gas, supply_exists, supply_avail = resource_paser.parse(frame)

        cv2.putText(frame, f'Frame number: {i} key_code:{key_code} {minerals}-{gas}-{supply_exists}-{supply_avail}', (10, 55),
                    FONT, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow(MainWindow.name, frame)

        key_code = cv2.waitKey(0)
        if key_code == 27:
            break
        elif key_code == 32:
            video_reader.next(100)

    video_reader.close()
