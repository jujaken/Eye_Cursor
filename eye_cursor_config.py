
from eye_cursor import Eye

red = (255, 0, 0)
blue = (0, 255, 0)

leftEye = Eye(0, 0, 0, 0, 0, 0, .007, red)
rightEye = Eye(0, 0, 0, 0, 0, 0, .007, blue)

primaryEye = leftEye
secondaryEye = rightEye

cam = 0
circleRadius = 3
frameScale = 2

draw = True
