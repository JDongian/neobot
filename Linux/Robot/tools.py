"""Convinience functions.
"""
import screen
import color
import matplotlib.pyplot as plot

#screen and game
def find_game(frame, identifiers, mode='pixel'):
    """Locates the game based on images of
    the upper left and bottom right corners.
    """
    if mode == 'pixel':
        return (color.find_pixels(identifiers[0], frame, 0, 'basic', 1)[0],
                color.find_pixels(identifiers[1], frame, 0, 'basic', 1)[1])
    elif mode == 'image':
        return (color.find_image(identifiers[0], frame,
                                 False, 0, 'forward', 1)[0],
                color.find_image(identifiers[1], frame,
                                 False, 0, 'backward', 1)[1])
    elif mode == 'scan':
        return find_game2(colorPair[0])
    else:
        print "ERROR: invalid mode."
        return False

def dist(p1, p2):
    """Return cartesian distance between two points.
    """
    return sum(((d[0]**2+d[1]**2) for d in zip(p1, p2)))**0.5

def find_game2(rgb, res=200, mode='x'):
    """Find a game using lines of color. Primarily for black.
    """
    lines = color.find_lines(rgb, 0, screen.get_screen(None, False, True),
                             res, mode)
    d = []
    dAvg = 0
    for l in lines:
        val = dist(l[0], l[1])
        if val > 1:
            d.append(val)
            dAvg += val
    dAvg /= float(len(d))
    begin = 0
    end = 0
    for i in xrange(len(lines)):
        if dist(lines[i][0], lines[i][1]) > dAvg:
            begin = lines[i][0]
            break
    for i in reversed(xrange(len(lines))):
        if dist(lines[i][0], lines[i][1]) > dAvg:
            end = lines[i][1]
            break
'''
    plot.plot(begin, end, 'ro')
    for l in lines:
        plot.plot((l[0][0], l[1][0]), (l[0][1], l[1][1]), 'b-')
    print "Done."
    plot.show()
'''
    #Return beginning and ending
    return (begin, end)
