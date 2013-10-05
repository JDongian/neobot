from ..Robot import tools
from ..Robot import robot
from ..Robot import screen
import time

game_url = 'http://www.neopets.com/games/play_flash.phtml?va=&game_id=805&nc_referer=&age=1&hiscore=300&sp=0&questionSet=&r=7795244&&width=909&height=660&quality=low'
game_colors = (179, 213, 218), (91, 135, 173)

ffStart = [(0.761, 0.681), (0.8642, 0.0365)]
ffSend = [(0.761, 0.681)]
ffRestart = [(0.751, 0.525)]
game_pos = (0,0)

def __init__():
    robot.rel_pos = tools.find_game(screen.get_screen()j
                                    ffStart, mode='pixel'):

def play(n=3, mode='farm'):
    for i in xrange(n):
        for p in ffStart:
            robot.click(p, 1, 'relative')
        for p in ffSend:
            robot.click(p, 1, 'relative')
        tool.restart_game(game_pos, ffRestart)
        if i != n-1:
            time.sleep(1)
            for p in ffRestart:
                robot.click(p, 1, 'relative')
                time.sleep(0.2)
