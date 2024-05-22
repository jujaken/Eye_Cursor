
from eye_cursor import *
from eye_cursor_config import *

app = EyeCursorApp(primaryEye, secondaryEye, circleRadius)
app.setput()

def exit():
    return cv2.waitKey(1) & 0xFF == ord('q')

while True:
    app.tick()
    app.moveCursor()
    app.useControls()
    if exit(): break
