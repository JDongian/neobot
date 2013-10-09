import time
from PIL import Image
import screen
import robot

def get_rgb(pos):
    display = screen.get_screen(None, False, True)
    return display.getpixel(pos)

old_rgb = get_rgb(robot.read_mouse_pos())
print old_rgb
while 1:
    time.sleep(0.05)
    new_rgb = get_rgb(robot.read_mouse_pos())
    if old_rgb != new_rgb:
        old_rgb = new_rgb
        print new_rgb
