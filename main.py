
from eye_cursor import *
from eye_cursor_config import *

app = EyeCursorApp(primaryEye, secondaryEye, cam)
app.frameScale = frameScale

if draw: app.setputGui(circleRadius)

def exit(): return cv2.waitKey(1) & 0xFF == ord('q')

while True:
    app.tick()
    if draw: app.drawGui()
    if exit(): break
