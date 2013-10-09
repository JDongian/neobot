from dogtail import rawinput
from dogtail import config
from Xlib import display
import time
import random

game_pos = 0

def __init__():
    config.config.defaults['defaultDelay'] = 0
    config.config.defaults['actionDelay'] = 0
    config.config.defaults['typingDelay'] = 0

def set_game_pos(pos):
    global gamePos
    game_pos = pos

###
### Keyboard out
###

def out_key(keyName, n=1, postdelay=0):
    '''
    Press the key n times.
    '''
    for i in range(n):
        rawinput.pressKey(keyName)
        time.sleep(postdelay)

def out_key_str(string, intradelay=0):
    '''
    Type the string with a given delay between each character.
    '''
    for char in string:
        outKey(char, 1, intradelay)

###
### Mouse in
###

def read_mouse_pos(screenroot=display.Display().screen().root):
    pointer = screenroot.query_pointer()
    data = pointer._data
    return data["root_x"], data["root_y"]

###
### Mouse out
###

def out_mouse_click(pos, mode):
    """Click in current position
    """
    if mode == 'current':
        return rawinput.click(*read_mouse_pos())
    elif mode == 'abs':
        return rawinput.click(*pos)
    #Click in the game using game-relative coordinates.
    elif mode == 'rel':
        if game_pos == 0:
            raise Exeption("Error: game_pos undefined.")
            return False
        #Bounds checking.
        if game_pos[0][0] <= pos[0] <= game_pos[1][0] and\
           game_pos[0][1] <= pos[1] <= game_pos[1][1]:
            return rawinput.click(game_pos[0][0]+pos[0],
                                  game_pos[0][1]+pos[1])
        else:
            raise Exeption("Error: position out of bounds.")
            return False
    elif mode == 'ratio':
        if game_pos == 0:
            raise Exeption("Error: game_pos undefined.")
            return False
        #Bounds checking.
        if 0 <= pos[0] <= 1 and\
           0 <= pos[1] <= 1:
            return rawinput.click(game_pos[0][0]+\
                                  pos[0]*(game_pos[1][0]-game_pos[0][0]),
                                  game_pos[0][1]+\
                                  pos[1]*(game_pos[1][1]-game_pos[0][1]))
        else:
            raise Exeption("Error: position out of bounds.")
            return False
    raise Exeption("Error: incorrect mode.")
    return False

def out_mouse_move(pos, mode):
    if mode == 'abs':
        return rawinput.absoluteMotion(*pos)
    #Click in the game using game-relative coordinates.
    elif mode == 'rel':
        if game_pos == 0:
            raise Exeption("Error: game_pos undefined.")
            return False
        #Bounds checking.
        if game_pos[0][0] <= pos[0] <= game_pos[1][0] and\
           game_pos[0][1] <= pos[1] <= game_pos[1][1]:
            return rawinput.absoluteMotion(game_pos[0][0]+pos[0],
                                           game_pos[0][1]+pos[1])
        else:
            raise Exeption("Error: position out of bounds.")
            return False
    elif mode == 'ratio':
        if game_pos == 0:
            raise Exeption("Error: game_pos undefined.")
            return False
        #Bounds checking.
        if 0 <= pos[0] <= 1 and\
           0 <= pos[1] <= 1:
            return rawinput.absoluteMotion(game_pos[0][0]+\
                                           pos[0]*(game_pos[1][0]-\
                                                   game_pos[0][0]),
                                           game_pos[0][1]+\
                                           pos[1]*(game_pos[1][1]-\
                                                   game_pos[0][1]))
        else:
            raise Exeption("Error: position out of bounds.")
            return False
    raise Exeption("Error: incorrect mode.")
    return False

"""Test suite
"""

def test_keyboard():
    print 'Testing kb out: printing alphabet twice.'
    for i in range(0, 26):
        outKey(chr(i+ord('a')))
    outStr(''.join(map(chr, range(97, 123))))

def test_mouse():
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
    test_mouse()
    test_keyboard()




