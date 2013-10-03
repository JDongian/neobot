"""Color analysis module
"""
from PIL import Image

#Pixel functions
def color_match(color_1, color_2, fuzz=0, mode='basic'):
    """Perform fuzzy color match with fuzziness parameter fuzz.
    Use 'basic' mode for unshared tolerence.
    Use 'conservative' for shared tolerence.
    Assume fuzz >= 0.
    by default, match colors stricly (fuzz=0).
    """
    #If there exists an r, g, or b value with
    #a difference greater than fuzz, abort.
    if mode == 'basic':
        for pigment_1, pigment_2 in zip(color_1, color_2):
            if abs(pigment_1-pigment_2) > fuzz:
                return False
        return True
    #If the the total difference in r, g, and b values
    #is greater than fuzz, abort.
    elif mode == 'conservative':
        for pigment_1, pigment_2 in zip(color_1, color_2):
            fuzz -= abs(pigment_1-pigment_2)
        if fuzz > 0:
            return True
        else:
            return False
    #Invalid color match mode. Abort!
    print "ERROR: invalid mode selected for color_match"
    return False

def get_current_screen_pixel(point, relative=False):
    '''Returns the pixel on the screen by coordinate.
    Setting parameter relative to True
    grabs with respect to the game position,
    as opposed to the top left corner.
    WARNING: The screen is grabbed on every call of this function.
    '''
    if relative == True:
        relative = get_game_pos()
        if x < 1:
            x = int(x*getGameDim()[0])
        if y < 1:
            y = int(y*getGameDim()[1])
        pos = (ref[0]+x, ref[1]+y)
    return ImageGrab.grab().getpixel(pos)

#Operations on multiple pixels
def find_pixels(rgb, rgb_domain, fuzz=0, mode='basic', limit=0):
    """Return coordinates of matching pixels in the domain.
    rgb_domain is a PIL RGB image.
    The limit parameter sets a limit on the number of pixels to return.
    """
    results = []
    for x in xrange(rgb_domain.size[0]):
        for y in xrange(rgb_domain.size[1]):
            if color_match(rgb, rgb_domain.getpixel((x,y)), fuzz, mode):
                results.append((x, y))
            if limit and (len(results) >= limit):
                return results
    return results

def find_color_region(rgb, size, rgb_domain,
                      fuzz=0, direction='forward', limit=0):
    """Find a rectangle of a given size of a given color in an image domain.
    Return x,y coordinate of matching regions.
    """
    rgb_target = Image.new('RGB', size, rgb)
    return find_image(rgb_target, rgb_domian, relRegion,
                      fuzz, direction, limit)

def image_at(rgb_target, rgb_domain, relPos, fuzz, direction):
    """Match an image in another image at a given point (relPos).
    """
    if direction == 'forward':
        #relPos is the top left corner
        for x in xrange(rgb_target.size[0]):
            for y in xrange(rgb_target.size[1]):
                if not color_match(rgb_target.getpixel((x, y)),
                                   rgb_domain.getpixel((x+relPos[0],
                                                        y+relPos[1])),
                                   fuzz, 'basic'):
                    return False
    elif direction == 'backward':
        #relPos is the bottom right corner
        for x in xrange(rgb_target.size[0]):
            for y in xrange(rgb_target.size[1]):
                if not color_match(rgb_target.getpixel((x, y)),
                                   rgb_domain.getpixel((x+relPos[0]-\
                                                        rgb_target.size[0],
                                                        y+relPos[1]-\
                                                        rgb_target.size[1])),
                                  fuzz, 'basic'):
                    return False
    else:
        print "ERROR: invalid direction"
        return False
    return True

def find_image(rgb_target, rgb_domain, region=False,
               fuzz=0, direction='forward', limit=0):
    """Find the first match of an search image
    in the specified region of a target image.
    If region is set to False, the entire target is searched.
    """
    if region == False:
        #Search the entire domain
        region = (rgb_domain.size[0], rgb_domain.size[1])
    if direction == 'forward':
        #Search from the top left corner.
        for x in xrange(region[0]):
            for y in xrange(region[1]):
                if isImageAt(rgb_target, rgb_domain, (x, y), fuzz, True):
                    return (x,y)
    elif direction == 'backward':
        #Search from the bottom right corner.
        #TODO: optimize?
        for x in reversed(xrange(rgb_target.size[0], region[0])):
            for y in reversed(xrange(rgb_target.size[1], region[1])):
                if isImageAt(rgb_target, rgb_domain, (x, y), fuzz, False):
                    return (x,y)
    return (-1,-1)

def find_lines(rgb_color, fuzz, rgb_domain,
               sweeps, mode):
    """Return start and endpoints of homogeneous color lines.
    """
    segments = []
    print 'Scanning...'
    step = max(1, int(rgb_domain.size[0 if\
                      mode == 'x' else 1]/(max(sweeps, 1))))
    for s in xrange(0, rgb_domain.size[0 if\
                      mode == 'x' else 1], step):
        curr_len = 0
        for l in xrange(0, rgb_domain.size[1 if\
                      mode == 'x' else 0]):
            if color_match(rgb_domain.getpixel((s,l)), rgb_color, fuzz):
                curr_len += 1
            else:
                if curr_len == 0:
                    continue
                segments.append(((s, l-curr_len) if\
                        mode == 'x' else (s-curr_len, l), (s,l)))
                curr_len = 0
                continue
                """
                elif thickness == 0:
                    segments.append(((s,l-currLen), (x,y)))
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
                """
    return segments
