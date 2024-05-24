
import cv2
import mediapipe as mp
import pyautogui

# init eye cursor modules

from eye_cursor import *

_FACE_W_LANDMARK_LEFT = 234
_FACE_W_LANDMARK_RIGHT = 454
_FACE_H_LANDMARK_UP = 10
_FACE_H_LANDMARK_DOWN = 152

# classes

class EyeLandmark:

    def __init__(self, name, id, color):
        self.name = name
        self.id = id
        self.color = color

    def isCorrect(self):
        return self.id > 0

    def landmark(self, landmarks):
        return landmarks[self.id]

    def pos(self, landmarks, fw, fh):
        landmark = self.landmark(landmarks)
        return int(landmark.x * fw), int(landmark.y * fh)

class Eye:

    lms = []

    # up - upper eyelid
    # down, left, right - parts of the pupil
    def __init__(self, lidUp : int, lidDown : int, center : int, up: int, down: int, left: int, right: int, eyeCloseDiv, color):
        self.lidUp = lidUp
        self._addLandMark('lidUp', lidUp, color)
        self.lidDown = lidDown
        self._addLandMark('lidDown', lidDown, color)
        self.center = center
        self._addLandMark('center', center, color)
        self.up = up
        self._addLandMark('up', up, color)
        self.down = down
        self._addLandMark('down', down, color)
        self.left = left
        self._addLandMark('left', left, color)
        self.right = right
        self._addLandMark('right', right, color)
        self.eyeCloseDiv = eyeCloseDiv
        self.color = color

    # private

    def _addLandMark(self, name, id, color):
        self.lms.append(EyeLandmark(name, id, color))

    def _faceLeft(self, lm): return lm[_FACE_W_LANDMARK_LEFT]
    
    def _faceRight(self, lm): return lm[_FACE_W_LANDMARK_RIGHT]
    
    def _faceUp(self, lm): return lm[_FACE_H_LANDMARK_UP]
    
    def _faceDown(self, lm): return lm[_FACE_H_LANDMARK_DOWN]

    def _faceW(self, lm):
        vec1 = self._faceLeft(lm)
        vec2 = self._faceRight(lm)
        return vec1, vec2
    
    def _faceH(self, lm):
        vec1 = self._faceUp(lm)
        vec2 = self._faceDown(lm)
        return vec1, vec2

    def _dist(self, v1, v2):
        return (v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2 + (v1.z - v2.z) ** 2

    # public

    def eyeLandmarks(self) -> list[EyeLandmark] :
        tbl = []
        for lm in self.lms: tbl.append(lm)
        return tbl
    
    def isOpen(self, landmarks) -> bool :
        distLidSqrl = self._dist(landmarks[self.lidUp], landmarks[self.lidDown])
        distPupilSqrl = self._dist(landmarks[self.up], landmarks[self.down])
        return distPupilSqrl / self.eyeCloseDiv > distLidSqrl

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

    def _calcW(self, x = 1):
        return self.fw * self.frameScale * x
    
    def _calcH(self, y = 1):
        return self.fh * self.frameScale * y

    def _drawAllLandmarks(self):
        for id, landmark in enumerate(self.lm):
            x = int(landmark.x * self._calcW())
            y = int(landmark.y * self._calcH())
            # cv2.circle(self.frame, (x, y), self.circleRadius, self.defaultColor)
            cv2.putText(self.frame, str(id), (x, y), 3, 0.5, self.defaultColor)

    def _drawFace(self, func):
        vec1, vec2 = func(self.lm)
        cv2.circle(self.frame, (int(self._calcW(vec1.x)), int(self._calcH(vec1.y))), 5, self.defaultColor)
        cv2.circle(self.frame, (int(self._calcW(vec2.x)), int(self._calcH(vec2.y))), 5, self.defaultColor)

    def _drawEyeLandmarks(self):
        for eye in [self.primaryEye, self.secondaryEye]:
            self._drawFace(eye._faceW)
            self._drawFace(eye._faceH)
            if eye.isOpen(self.lm): cv2.circle(self.frame, (25, 25), 20, eye.color)
            for eyeLandmark in eye.eyeLandmarks():
                if not eyeLandmark.isCorrect(): continue
                x, y = eyeLandmark.pos(self.lm, self._calcW(), self._calcH())
                cv2.circle(self.frame, (x, y), self.circleRadius, eyeLandmark.color)

    def _clickControl(self, eye : Eye, name : str):
        (eye.isOpen() and pyautogui.mouseDown or pyautogui.mouseUp)(button=name)

    # public:

    def updateLandmarks(self):
        self._updateFrame()
        lm = self.fm.process(self.rgb_frame).multi_face_landmarks
        self.lm = lm and lm[0].landmark

    def useCursor(self):
        pass
    
    def useControls(self):
        self._clickControl(self.primaryEye, 'primary')
        self._clickControl(self.secondaryEye, 'secondary')

    def tick(self):
        self.updateLandmarks()
        self.useCursor()
        # self.useControls()

    def setputGui(self, circleRadius, defaultColor = (0, 0, 255)):
        self.circleRadius = circleRadius
        self.defaultColor = defaultColor
        pyautogui.FAILSAFE = True
        
    def drawGui(self, all = False):
        self.frame = cv2.resize(self.frame, (self._calcW(), self._calcH()))
        if self.lm: (all and self._drawAllLandmarks or self._drawEyeLandmarks)()
        cv2.imshow('Eye Cursor', self.frame)
        cv2.waitKey(1)
