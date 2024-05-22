
import cv2
import mediapipe as mp
import pyautogui

# init eye cursor modules

from eye_cursor import *

# classes

class EyeLandmark:

    def __init__(self, name, id, color):
        self.name = name
        self.id = id
        self.color = color

    def isCorrent(self):
        return self.id > 0

    def landmark(self, landmarks):
        return landmarks[self.id]

    def pos(self, landmarks, fw, fh):
        landmark = self.landmark(landmarks)
        return int(landmark.x * fw), int(landmark.y * fh)

class Eye:

    def __init__(self, up: int, down: int, left: int, right: int, minDist, color):
        self.up = EyeLandmark('up', up, color)
        self.down = EyeLandmark('down', down, color)
        self.left = EyeLandmark('left', left, color)
        self.right = EyeLandmark('right', right, color)
        self.minDist = minDist
        self.color = color

    def eyeLandmarks(self) -> list[EyeLandmark] :
        tbl = []
        if self.up.isCorrent(): tbl.append(self.up)
        if self.down.isCorrent(): tbl.append(self.down)
        if self.left.isCorrent(): tbl.append(self.left)
        if self.right.isCorrent(): tbl.append(self.right)
        return tbl
    
    def center(self, landmarks):
        return (0, 0)
    
    def isOpen(self, landmarks) -> bool :
        return True

class EyeCursorApp:

    def __init__(self, primaryEye, secondaryEye):
        self.primaryEye, self.secondaryEye = primaryEye, secondaryEye
        self.fm = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.sh, self.sw = pyautogui.size()
        self.cam = cv2.VideoCapture(0)

    # private: 

    def _updateFrame(self):
        _, self.frame = self.cam.read()
        self.frame = cv2.flip(self.frame, 1)
        self.fh, self.fw, _ = self.frame.shape
        self.rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def _drawAllLandmarks(self):
        for id, landmark in enumerate(self.lm):
            x = int(landmark.x * self.fw)
            y = int(landmark.y * self.fh)
            # cv2.circle(self.frame, (x, y), self.circleRadius, self.defaultColor)
            cv2.putText(self.frame, str(id), (x, y), 1, 0.35, self.defaultColor)

    def _drawEyeLandmarks(self):
        for eye in [self.primaryEye, self.secondaryEye]:
            for eyeLandmark in eye.eyeLandmarks():
                x, y = eyeLandmark.pos(self.lm, self.fw, self.fh)
                cv2.circle(self.frame, (x, y), self.circleRadius, eyeLandmark.color)

    def _clickControl(eye : Eye, name : str):
        (eye.isOpen() and pyautogui.mouseDown or pyautogui.mouseUp)(button=name)

    # public:

    def updateLandmarks(self):
        self._updateFrame()
        lm = self.fm.process(self.rgb_frame).multi_face_landmarks
        self.lm = lm and lm[0].landmark

    def useCursor(self):
        pass
    
    def useControls(self):
        pass

    def tick(self):
        self.updateLandmarks()
        self.useCursor()
        self.useControls()

    def setputGui(self, circleRadius, defaultColor = (0, 0, 255)):
        self.circleRadius = circleRadius
        self.defaultColor = defaultColor
        pyautogui.FAILSAFE = True
        
    def drawGui(self):
        if self.lm: (all and self._drawAllLandmarks or self._drawEyeLandmarks)()
        cv2.imshow('Eye Cursor', self.frame)
        cv2.waitKey(1)
