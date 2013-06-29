import requests
import re

hideURL = 'http://www.neopets.com/games/process_hideandseek.phtml'

def play(session):
    for i in xrange(1, 16):
        query = {'p':i 'game':17}
        hidePage = session.get(hideURL, query).content
        result = re.findall('You win <b>(\d+)', result):
        if(result):
            return result[0]



