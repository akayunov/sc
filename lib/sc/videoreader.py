import cv2
from .const import MainWindow, FONT


class VideoReader:
    def __init__(self, file_name):
        self.cur_frame_number = 1100
        self.cap = cv2.VideoCapture(file_name)
        ret, self.frame = self.cap.read()
        if not ret:
            raise Exception('Not ret')
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_number)
        self.cur_frame_number += 1
        self.gen = self._gen()
        self.gen.send(None)
        cv2.setMouseCallback(MainWindow.name, self.mouse_callback)

    def _gen(self):
        while True:
            flag = yield self.cur_frame_number, self.frame
            if flag == 'break':
                break
            elif isinstance(flag, int):
                self.cur_frame_number += flag - 1
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.cur_frame_number)

            ret, frame = self.cap.read()
            if not ret:
                raise Exception('Not ret')
            self.cur_frame_number += 1
            self.frame = frame

    def next(self, pass_frame_count=1, break_read=False):
        if break_read:
            self.gen.send('break')
        return self.gen.send(pass_frame_count)

    def mouse_callback(self, event, x, y, flags, param):
        frame = self.frame.copy()
        if event == cv2.EVENT_LBUTTONDOWN:
            # if event == cv2.EVENT_MOUSEMOVE:
            b, g, r = frame[y, x]
            cv2.putText(frame, f'mouse: {x} {y} b:{b} g:{g} r:{r}', (10, 115), FONT, 1, (0, 255, 0), 2, cv2.LINE_AA)
            for i in range(100):
                for k in range(100):
                    frame[i][k] = (b, g, r)
            cv2.imshow(MainWindow.name, frame)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()