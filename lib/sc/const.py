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


@dataclass
class _ScreenSize:
    width: int = 1280
    heigth: int = 720


ScreenSize = _ScreenSize()


@dataclass
class _MiniMapSize:
    x: int = 547
    x_shift: int = 153
    y: int = 19
    y_shift: int = 175


MiniMapSize = _MiniMapSize()
