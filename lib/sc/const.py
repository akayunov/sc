from dataclasses import dataclass
from pathlib import Path
import cv2

RESOURCE_DIR = str(Path(Path(__file__).parent, 'resources'))
FONT = cv2.FONT_HERSHEY_SIMPLEX


@dataclass
class MainWindow:
    name: str = 'main'
    scale_x: int = 1
    scale_y: int = 1
    cv2.namedWindow(name)


@dataclass
class DebugWindow:
    name: str = 'debug'
    scale_x: int = 3
    scale_y: int = 3
    cv2.namedWindow(name)
