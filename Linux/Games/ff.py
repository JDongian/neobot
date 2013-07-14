from ..Robot import robot
from ..Robot import visual

url = 'http://www.neopets.com/games/play_flash.phtml?va=&game_id=805&nc_referer=&age=1&hiscore=300&sp=0&questionSet=&r=7795244&&width=909&height=660&quality=low'
gameColors = (179, 213, 218), (91, 135, 173)

ffStart = [(0.761, 0.681), (0.8642, 0.0365)]
ffSend = [(0.761, 0.681)]
ffRestart = [(0.751, 0.525)]

def play(n=3, mode='farm'):
    robot.setGamePos(visual.findGame(gameColors))
    return
    for i in range(n):
        print 'Starting game...'
        for p in ffStart:
            clickRel(p, 1)
        print 'Submitting score...'
        for p in ffSend:
            clickRel(p, 1)
        restartX = int(ffRestart[0][0]*getGameDim()[0])
        restartY = int(ffRestart[0][1]*getGameDim()[1])
        box = ((restartX-20, restartY-10), (restartX+20, restartY+10))
        print 'Waiting for submission...'
        while findColor((255, 255, 255), 5, True, (1,1),
                ((restartX-20, restartY-10), (restartX+20, restartY+10)),
                getGamePos()[0]) == (-1,-1):
            print 'Waiting for submission...'
            wait(0.2, 0)
        print 'Score submitted.'
        if i != n-1:
            print 'Restarting game...'
            wait(1, 0.1)
            traversePath(ffRestart, 0.2, True, getGamePos()[0])

if __name__=='__main__':
    '''
    import time
    import sys
    time.sleep(1)
    if sys.argv:
        play(sys.argv[0])
    else:
        play()
    '''
    print 'herp'
