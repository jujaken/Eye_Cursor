
from eye_cursor import Eye

green = (255, 0, 0)
blue = (0, 255, 0)

rightEye = Eye(386, 374, 473, 475, 477, 476, 474, 5, blue)
leftEye = Eye(159, 145, 468, 470, 472, 471, 469, 5, green)

primaryEye = leftEye
secondaryEye = rightEye

cam = 0
circleRadius = 3
frameScale = 2

draw = True
