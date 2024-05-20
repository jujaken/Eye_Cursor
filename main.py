import cv2
import mediapipe as mp
import pyautogui

fm = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
sh, sw = pyautogui.size()

pyautogui.FAILSAFE = True

cam = cv2.VideoCapture(0)
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = fm.process(rgb_frame)
    lm = output.multi_face_landmarks
    fh, fw, _ = frame.shape
    if lm:
        landmarks = lm[0].landmark
        right = landmarks[474:478]
        for id, landmark in enumerate(right):
            x: int = int(landmark.x * fw)
            y: int = int(landmark.y * fh)
            if id == 1:
                # DOTO: create trace 
                sx = int(2 * (landmark.x * sw))
                sy = int(2 * (landmark.y * sh))
                print(sx, sy)
                pyautogui.moveTo(sx, sy)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
            else:
                cv2.circle(frame, (x, y), 3, (255, 255, 0))
            
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * fw)
            y = int(landmark.y * fh)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        # print(left[0].y - left[1].y)
        leftEyeIsClose = left[0].y - left[1].y < 0.007
        rightEyeIsOpen = right[0].y - right[1].y > 0.007
        if leftEyeIsClose and rightEyeIsOpen:
            pyautogui.mouseDown()
            pyautogui.sleep(0.5)
        else:
            pyautogui.mouseUp()
    cv2.imshow('Eye Cursor', frame)
    cv2.waitKey(1)
