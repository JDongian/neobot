"""Screen scraping functionality
"""
from gtk import gdk
from PIL import Image
from collections import namedtuple
import time
import random

Point = namedtuple('Point', ['x', 'y'])

def get_window():
    """Return root window.
    """
    return gdk.get_default_root_window()

def _pixbuf_to_image(pb):
    """Convert a gdk pixbuf to a PIL image.
    """
    return Image.frombuffer('RGB', (pb.get_width(), pb.get_height()),
                            pb.get_pixels(), 'raw', 'RGB',
                            pb.get_rowstride(), 1)

def _gdk_pull_region(window, offset=Point(0,0), dim=Point(0,0)):
    """Return a region of the screen using gdk.
    """
    pb = gdk.Pixbuf(gdk.COLORSPACE_RGB, False, 8, dim.x, dim.y)
    pb = pb.get_from_drawable(window, window.get_colormap(),
                              offset.x, offset.y, 0, 0, dim.x, dim.y)
    return _pixbuf_to_image(pb)

'''
def _gdk_pull_screen(window, save_screen=False):
    """Get entire screen using gdk.
    Optionally save the screen into ./last_frame.png.
    """
    screen = _gdk_pull_region(window, Point(0,0), Point(*window.get_size()))
    if save_screen:
        pb.save("./last_frame.png","png")
    return screen
'''

def get_screen(region, window=False, grab_all=False):
    """Screen capture wrapper function.
    Input is a region consisting of
    a pair of Points, top left and bottom right.
    """
    #Eventually, add support for negative region dimensions
    #For Linux, gdk pull screen seems to work.
    if not window:
        window = get_window()
    if grab_all:
        return _gdk_pull_region(window, Point(0,0), Point(*window.get_size()))
    else:
        return _gdk_pull_region(_get_window(),
                                Point(*region[0]),
                                Point(abs(region[1][0]-region[1][1],
                                      abs(region[1][0]-region[1][1]))))

if __name__ == '__main__':
    get_screen().show()
