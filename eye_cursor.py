
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

    lms = []

    def _addLandMark(self, name, id, color):
        self.lms.append(EyeLandmark(name, id, color))

    # up - upper eyelid
    # down, left, right - parts of the pupil
    def __init__(self, lid : int, center : int, up: int, down: int, left: int, right: int, minDist, color):
        self._addLandMark('lid', lid, color)
        self._addLandMark('center', center, color)
        self._addLandMark('up', up, color)
        self._addLandMark('down', down, color)
        self._addLandMark('left', left, color)
        self._addLandMark('right', right, color)
        self.minDist = minDist
        self.color = color

    def eyeLandmarks(self) -> list[EyeLandmark] :
        tbl = []
        for lm in self.lms: tbl.append(lm)
        return tbl
    
    def isOpen(self, landmarks) -> bool :
        return True

class EyeCursorApp:

    frameScale = 1

    def __init__(self, primaryEye, secondaryEye, cam):
        self.primaryEye, self.secondaryEye = primaryEye, secondaryEye
        self.fm = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.sh, self.sw = pyautogui.size()
        self.cam = cv2.VideoCapture(cam)

    # private: 

    def _updateFrame(self):
        _, self.frame = self.cam.read()
        self.frame = cv2.flip(self.frame, 1)
        self.fh, self.fw, _ = self.frame.shape
        self.rgb_frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

    def _calcW(self):
        return self.fw * self.frameScale
    
    def _calcH(self):
        return self.fh * self.frameScale

    def _drawAllLandmarks(self):
        for id, landmark in enumerate(self.lm):
            x = int(landmark.x * self._calcW())
            y = int(landmark.y * self._calcH())
            # cv2.circle(self.frame, (x, y), self.circleRadius, self.defaultColor)
            cv2.putText(self.frame, str(id), (x, y), 3, 0.25, self.defaultColor)

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
        self.frame = cv2.resize(self.frame, (self._calcW(), self._calcH()))
        if self.lm: (all and self._drawAllLandmarks or self._drawEyeLandmarks)()
        cv2.imshow('Eye Cursor', self.frame)
        cv2.waitKey(1)
