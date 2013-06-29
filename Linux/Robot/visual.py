import gtk.gdk#
from PIL import Image
import time
import random

window, screenSize = 0,0
currentFrame = False

def pixbufToImage(pb):#
    return Image.frombuffer('RGB', (pb.get_width(), pb.get_height()),
            pb.get_pixels(), 'raw', 'RGB', pb.get_rowstride(), 1)
    #return Image.fromstring('RGB', (pb.get_width(), pb.get_height()), pb.get_pixels() )

def init():
    global window, screenSize
    window = gtk.gdk.get_default_root_window()
    screenSize = window.get_size()

def updateScreen():
    global currentFrame
    currentFrame = getScreen()

def getScreen():
    pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,screenSize[0],screenSize[1])
    pb = pb.get_from_drawable(window,window.get_colormap(),0,0,0,0,screenSize[0],screenSize[1])
    if (pb != None):
        #pb.save("./test.png","png")
        return pixbufToImage(pb)
    else:
        return False

#Color Analysis
def isColorMatch(c1, c2, fuzz=0, mode='basic'):
    '''
    Perform fuzzy color match with rgb difference fuzz.
    Use 'basic' mode for unshared tolerence.
    Use 'conservative' for shared tolerence.
    '''
    if fuzz < 0:
        print 'Error: bad fuzz parameter.'
    if mode == 'basic':
        for b1, b2 in zip(c1, c2):
            if abs(b1-b2) > fuzz:
                return False
        return True
    elif mode == 'conservative':
        for i, j in zip(c1, c2):
            fuzz -= abs(c1[i]-c2[j])
        if fuzz >= 0:
            return True
        else:
            return False
def getColor((x,y), ref=False, im=False):
    '''
    Returns the color of the pixel on the screen.
    If ref is set to False, the position is in-game position.
    WARNING: the screen is grabbed on every call of this function.
    '''
    if ref == False:
        ref = getGamePos()
        if x<1:
            x = int(x*getGameDim()[0])
        if y<1:
            y = int(y*getGameDim()[1])
        pos = (ref[0]+x, ref[1]+y)
    ####win32api.SetCursorPos(pos)
    ####time.sleep(0.2)
    if im == False:
        return ImageGrab.grab().getpixel(pos)
    else:
        return im.getpixel(pos)
def findPixels(rgb, rgb_domain, fuzz=0):
    '''
    Returns a list of coordinates of matching pixels in the domain.
    '''
    results = []
    for x in xrange(rgb_domain.size[0]):
        for y in xrange(rgb_domain.size[1]):
            if isColorMatch(rgb, rgb_domain.getpixel((x,y)), fuzz):
                results.append((x, y))
    return results

def findColor(rgb, size, rgb_domain, relRegion=False,
              fuzz=0, forward=True):
    '''
    Find a rectangle of color in an image.
    '''
    rgb_target = Image.new('RGB', size, rgb)
    return findImage(rgb_target, rgb_domian, relRegion, fuzz, forward)
def findColorOnScreen(rgb, size=(1,1),
                      fuzz=0, forward=True):
    '''
    Find a rectangle of color on the current frame.
    '''
    rgb_target = Image.new('RGB', size, rgb)
    return findImage(rgb_target, currentFrame, False, fuzz, forward)

#Image matching
def isImageAt(rgb_target, rgb_domain, relPos, fuzz, forward=True):
    '''
    Match an image in another image at a given point (relPos).
    '''
    if forward:
        #relPos is the top left corner
        for x in range(rgb_target.size[0]):
            for y in range(rgb_target.size[1]):
                if not isColorMatch(rgb_target.getpixel((x, y)),
                                  rgb_domain.getpixel((x+relPos[0], y+relPos[1])),
                                  fuzz, 'basic'):
                    return False
    else:
        #relPos is the bottom right corner
        for x in range(rgb_target.size[0]):
            for y in range(rgb_target.size[1]):
                if not isColorMatch(rgb_target.getpixel((x, y)),
                                  rgb_domain.getpixel((x+relPos[0]-rgb_target.size[0],
                                                    y+relPos[1]-rgb_target.size[1])),
                                  fuzz, 'basic'):
                    return False
    return True

def findImage(rgb_target, rgb_domain, region=False,
              fuzz=0, forwardSearch=True):
    '''
    Find the first match of an search image
    in the specified region of a target image.
    If region is set to False, the entire target is searched.
    '''
    if region == False:
        #Search the entire domain
        region = (rgb_domain.size[0], rgb_domain.size[1])
    if forwardSearch:
        #Search from the top left corner.
        for x in xrange(region[0]):
            for y in xrange(region[1]):
                if isImageAt(rgb_target, rgb_domain, (x, y), fuzz, True):
                    return (x,y)
    else:
        #Search from the bottom right corner.
        for x in reversed(range(rgb_target.size[0])):
            for y in reversed(range(rgb_target.size[1])):
                if isImageAt(rgb_target, rgb_domain, (x, y), fuzz, False):
                    return (x,y)
    return (-1,-1)
def findImageOnScreen(rgb_target, region=((0,0), (1366,768)),
                      fuzz=0, forwardSearch=True):
    '''
    Scrapes a region of the screen to find an image
    '''
    box = (region[0][0], region[0][1],
           region[1][0], region[1][1])
    search = getScreen().crop(box)
    if forwardSearch:
        return findImage(rgb_im, search, (0,0), fuzz, True)
    else:
        return findImage(rgb_im, search, (search.size[0], search.size[1]), fuzz, False)
def findThick(color, fuzz, rgb_im, im_pos,
              sweeps, thickness, errorOver, errorUnder, mode):
    '''
    Return start and endpoints of homogeneous color lines.
    mode = 'x' for vertical sweeps
    mode = 'y' for horizontal sweeps
    rgb_im = 0 for all screen
    sweeps = 0 for sweeping every pixel
    thickness = 0 for all results
    '''
    segments = []
    if rgb_im == 0:
        rgb_im = ImageGrab.grab()
    if mode == 'x':
        print 'vertical scan'
        step = int(rgb_im.size[0]/(sweeps+1))
        if step < 1 or sweeps == 0:
            step = 1
        for x in range(0, rgb_im.size[0], step):
            currLen = 0
            for y in range(0, rgb_im.size[1]):
                win32api.SetCursorPos((x+im_pos[0]+1, y+im_pos[1]+1))
                if fuzzyMatch(rgb_im.getpixel((x,y)), color, fuzz):
                    currLen += 1
                else:
                    if currLen == 0:
                        continue
                    elif thickness == 0:
                        segments.append(((x,y-currLen), (x,y)))
                        currLen = 0
                        continue
                    elif (thickness-errorUnder > currLen) or\
                       (thickness+errorOver < currLen):
                        currLen = 0
                        continue
                    else:
                        segments.append(((x,y-currLen), (x,y)))
                        count = 0
                        continue
    if mode == 'y':
        print 'horizontal scan'
        step = int(rgb_im.size[1]/(sweeps+1))
        if step < 1 or sweeps == 0:
            step = 1
        for y in range(0, rgb_im.size[1], step):
            currLen = 0
            for x in range(0, rgb_im.size[0]):
                win32api.SetCursorPos((x+im_pos[0]+1, y+im_pos[1]+1))
                if fuzzyMatch(rgb_im.getpixel((x,y)), color, fuzz):
                    currLen += 1
                else:
                    if currLen == 0:
                        continue
                    elif thickness == 0:
                        segments.append(((x-currLen,y), (x,y)))
                        currLen = 0
                        continue
                    elif (thickness-errorUnder > currLen) or\
                       (thickness+errorOver < currLen):
                        currLen = 0
                        continue
                    else:
                        segments.append(((x-currLen,y), (x,y)))
                        count = 0
                        continue
    return segments

#screen and game
def findGame(colorPair):
    '''
    Locates the game based on images of
    the upper left and bottom right corners.
    '''
    global currentFrame
    currentFrame = getScreen()
    return (findColorOnScreen(colorPair[0], (1,1), True, (1,1)),
            findColorOnScreen(colorPair[1], (1,1), False, (1,1)))

def findGame2(color, res=200, mode='x'):
    lines = findThick(color, 0, 0, (0,0), res, 0, 0, 0, mode)
    d = []
    for l in lines:
        val = dist(l[0], l[1])
        if val > 1:
            d.append(val)
    dAvg = avg(d)*1
    begin = 0
    end = 0
    for i in range(len(lines)):
        if dist(lines[i][0], lines[i][1]) > dAvg:
            begin = lines[i][0]
            break
    for i in reversed(range(len(lines))):
        if dist(lines[i][0], lines[i][1]) > dAvg:
            end = lines[i][1]
            break
##    print begin, end
##    print lines
##    import grapher
##    grapher.setData('screen', lines, [], [begin, end], 0.8)
##    grapher.main()    
    gamePos = (begin, end)
    gameLen = gamePos[1][0]-gamePos[0][0]
    gameHeight = gamePos[1][1]-gamePos[0][1]

def getScreenSize():
    return screenSize


init()

"""
DEBUGGING TOOLS
"""
def saveScreen():
    '''
    TODO: add id number for multiple screenshots
    '''
    currentFrame.save('./screenshots/scr.png')

def showImg(name):
    Image.open(name).show()

def test():
    print 'true:', isColorMatch((0,0,0), (0,0,0))
    print 'false:', isColorMatch((0,0,1), (0,0,0))
    print 'true:', isColorMatch((0,0,0), (5,5,5), 5)
    print 'false:', isColorMatch((0,0,0), (6,5,5), 5)
    updateScreen()
    saveScreen()
    print currentFrame.getpixel((0,0))
    #print len(findPixels((0,0,0), currentFrame, 1))
    print 'first instance of black:', findColorOnScreen((0,0,0), (1,1))
    #print 'last instance of black:', findColorOnScreen((0,0,0), (1,1), 0, False)
    #showImg('./screenshots/scr.png')

if __name__=='__main__':
    test()

