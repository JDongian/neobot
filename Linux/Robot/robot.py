from dogtail import rawinput
from dogtail import config
from Xlib import display
import time
import random


config.config.defaults['defaultDelay'] = 0
config.config.defaults['actionDelay'] = 0
config.config.defaults['typingDelay'] = 0

###
### Keyboard out
###

def outKey(keyName, n=1, postdelay=0):
    '''
    Press the key n times.
    '''
    for i in range(n):
        rawinput.pressKey(keyName)
        time.sleep(postdelay)

def outStr(string, intradelay=0):
    '''
    Type the string with a given delay between each character.
    '''
    for char in string:
        outKey(char, 1, intradelay)

###
### Mouse in
###

def getMousePos(screenroot=display.Display().screen().root):
    pointer = screenroot.query_pointer()
    data = pointer._data
    return data["root_x"], data["root_y"]

###
### Mouse out
###

def outClick(postDelay=0):
    '''
    Click in current position
    '''
    clickAbs(mousePos(), postDelay)

def outMov(coord, mode, click=False, postDelay=0):
    global gamePos

    if mode == 'abs':
        rawinput.absoluteMotion(coord[0], coord[1], postDelay)
    elif mode == 'rel':
        rawinput.absoluteMotion((int(gamePos[0][0]+relPos[0]),
            int(gamePos[0][1]+relPos[1])), postDelay)
    elif mode == 'ratio':
        rawinput.absoluteMotion((int(ratioPos[0]*gameLen),
            int(ratioPos[1]*gameHeight)), postDelay)
    if click:
        outClick(postDelay)

def clickAbs(absPos, postDelay=0):
    '''
    Click on the computer screen.
    '''
    return rawinput.click(absPos[0], absPos[1])

def clickRel(relPos, downTime):
    '''
    Click in the game using game-relative coordinates.
    '''
    global gamePos

    if gamePos == -1:
        print 'Error: gamePos undefined.'
        return False
    if relPos[0] > gamePos[1][0] or relPos[1] > gamePos[1][1]:
        print 'Error: position out of bounds.'
        return False
    return clickAbs((int(gamePos[0][0]+relPos[0]), int(gamePos[0][1]+relPos[1])),
              downTime)

def clickRatio(ratioPos, downTime):
    '''
    Click in the game with a xy-ratio input.
    '''
    global gameLen
    global gameHeight
    if gameLen == -1 or gameHeight == -1:
        print 'Error: game dimensions undefined.'
        return False
    return clickRel((ratioPos[0]*gameLen, ratioPos[1]*gameHeight), downTime)

def traversePath(points, click=False, ref=-1):
    '''
    Traverse the given game path.
    Do not mix ratio and relative point formats.
    Set click to True to click at each point on the path.
    '''
    global gamePos
    if ref == -1:
        ref = gamePos
    mode = 'absolute'
    if 0 < points[0][0] < 1:
        mode = 'ratio'
    for p in points:
        if mode == 'ratio':
            pos = int(p[0]*gameLen)+ref[0], int(p[1]*gameHeight)+ref[1]
        else:
            pos = p[0]+ref[0], p[1]+ref[1]
        rawinput.absoluteMotion(pos[0], pos[1])
        if click:
            click()

def randomizePoint(p, dx, dy):
    return p+random.gauss(0, dx/4), p+random.gauss(0, dy/4)

def randomWait(t):
    print 'I waited'

'''
Test suite
'''

def testKb():
    print 'Testing kb out: printing alphabet twice.'
    for i in range(0, 26):
        outKey(chr(i+ord('a')))
    outStr(''.join(map(chr, range(97, 123))))

def testMouse():
    import subprocess, re
    print 'Testing mouse out: drawing a square spiral.'
    osval = subprocess.check_output("xrandr | grep '*'", shell=True)
    dim = re.findall('(\d+)', osval)[:2]
    dim = int(dim[0]), int(dim[1])
    counter = 0
    while counter < dim[1]:
        outMov((counter, counter), 'abs')
        outMov((counter, dim[1]-counter), 'abs')
        outMov((dim[0]-counter, dim[1]-counter), 'abs')
        outMov((dim[0]-counter, counter), 'abs')
        counter += 1
    for i in xrange(400):
        outMov((i*2,i), 'abs', False, 0.05)

if __name__=='__main__':
    testMouse()
    testKb()




