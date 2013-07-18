import operator
import re
import requests
import json
import getpass
from bs4 import BeautifulSoup
import datetime
from pprint import pprint

lunarGetURL = 'http://www.neopets.com/shenkuu/lunar/?show=puzzle'
lunarPostURL = 'http://www.neopets.com/shenkuu/lunar/results.phtml'
omeletteURL = 'http://www.neopets.com/prehistoric/omelette.phtml'
jellyURL = 'http://www.neopets.com/jelly/jelly.phtml'
bankPostURL = 'http://www.neopets.com/process_bank.phtml'
bankGetURL = 'http://www.neopets.com/bank.phtml'
slorgURL = 'http://www.neopets.com/shop_of_offers.phtml'
toyURL = 'http://www.neopets.com/petpetpark/daily.phtml'
obsidianURL = 'http://www.neopets.com/magma/quarry.phtml'
appleURL = 'http://www.neopets.com/halloween/applebobbing.phtml?bobbing=1'
krawkenURL = 'http://www.neopets.com/pirates/anchormanagement.phtml'
marrowURL = 'http://www.neopets.com/medieval/process_guessmarrow.phtml'
tombolaURL = 'http://www.neopets.com/island/tombola2.phtml'
tombURL = 'http://www.neopets.com/worlds/geraptiku/process_tomb.phtml'
fruitURL = 'http://www.neopets.com/desert/fruit/index.phtml'
coltzanURL = 'http://www.neopets.com/desert/shrine.phtml'
meteorURL = 'http://www.neopets.com/moon/process_meteor.phtml'
plushieURL = 'http://www.neopets.com/faerieland/tdmbgpop.phtml'
fishingURL = 'http://www.neopets.com/water/fishing.phtml'
hideURL = 'http://www.neopets.com/games/process_hideandseek.phtml'
DP_URL = 'http://www.neopets.com/community/index.phtml'
crossword_URL = 'http://www.neopets.com/games/crossword/crossword.phtml'

answers_URL = 'http://www.tdnforums.com/index.php?/rss/forums/3-faerie-crossword-answers-from-tdn/'


def hide(session):
    '''
    needs testing
    '''
    for i in range(1, 16):
        query = {'p':i,'game':17}
        hidePage = session.get(hideURL+'?p='+str(i)+'&game=17').content
        result = re.findall('You win <b>(\d+)', hidePage)
        if(result):
            print 'win'
            return result
        else:
            print 'no: '
            return hidePage
    return False

def metor(session):
    query = {'pickstep':1, 'meteorSubmit':'Submit'}
    meteorPage = session.post(meteorURL, query)
    if(re.findall('dream', meteorURL)):
        return False
    return True
def marrow(session):
    '''
    Needs avail. checking
    '''
    query = {'guess':642}
    #query = {'guess':int(raw_input('Marrow weight? '))}
    marrowPage = session.post(marrowURL, query).content
    if(re.findall('WRONG!', marrowPage)):
        return False
    return True


'''
Helper functions
'''

def _get_DP():
    answer_page = requests.get(answers_URL).content
    answer = re.findall('</strong> ([A-Z0-9].*?)<br', answer_page)
    date = re.findall('<title>.*?(\d+).*?</title', answer_page)
    if answer and date:
        return answer[0], date[0]
    else:
        return False

def _get_crossword():
    answer_page = requests.get(answers_URL).content
    across = re.findall('Across:</strong><br />\s+([^`]*?)\s*<td', answer_page)
    down = re.findall('Down:</strong><br />\s+([^`]*?)\s*<td', answer_page)
    if across and down:
        return [re.findall('(\d+)\.\s+(.*?)<br', across[0]),
                re.findall('(\d+)\.\s+(.*?)<br', down[0])]
    else:
        return False

'''
(MOSTLY) FINISHED METHODS
'''

def get_crossword(session, header={}):
    header['Referer'] = 'http://www.neopets.com/games/crossword/index.phtml'
    crossword = session.post(crossword_URL, headers=header).content
    soup = BeautifulSoup(crossword)

    crossword_table = soup.find_all('table', width=455, height=455)[0]
    rows = crossword_table.find_all('tr')

    crossword_model = []
    for r in rows:
        current_row = []
        for e in r.find_all('td'):
            if e.find_all('a'):
                current_row.append(str(e['background'])[-6:-4])
            else:
                current_row.append('  ')
        crossword_model.append(current_row)
    #print ''
    #for r in crossword_model: print r

    answers = _get_crossword()
    answers = zip(answers[0], ['across']*len(answers[0]))+zip(answers[1], ['down']*len(answers[1]))
    #print answers

    crossword_positions = {}
    for row in xrange(len(crossword_model)):
        for col in xrange(len(crossword_model[0])):
            current = crossword_model[row][col]
            if current == '  ':
                continue
            elif current != 'll':
                if row < len(crossword_model)-1:
                    if crossword_model[row+1][col] == 'll':
                        crossword_positions[current+u' down'] =  col, row
                if col < len(crossword_model[0])-1:
                    if crossword_model[row][col+1] == 'll':
                        crossword_positions[current+u' across'] = col, row
    #pprint(crossword_positions)

    header['Referer'] = 'http://www.neopets.com/games/crossword/crossword.phtml'
    for ans, direction in sorted(answers, key=lambda x: int(x[0][0])):
        print ans, direction
        query = {
            'x_word': ans[1],
            'showclue': ans[0]+' '+direction,
            'x_clue_row': crossword_positions[ans[0].zfill(2)+' '+direction][1]+1,
            'x_clue_col': crossword_positions[ans[0].zfill(2)+' '+direction][0]+1,
            'x_clue_dir': (lambda f: {'across': 1, 'down': 2}[f])(direction)
        }
    #    print query
        crossword_page = session.post(crossword_URL, query, headers=header).content
        with open('dump/dumpCrosswords.html', 'w') as dump:
            dump.write(crossword_page.encode('ascii', 'xmlcharrefreplace'))
    if 1:
        return True

def get_puzzle(session):
    answer, neodate = _get_DP()
    question_page = requests.get(DP_URL).content
    answer = re.findall('\'(\d)\'>'+answer+'</option>', question_page)[0]
    print answer
    query = {
        'trivia_date': str(datetime.date.today())[:-2]+neodate,
        'trivia_response': int(answer),
        'submit': 'Submit'
    }
    header = {'Referer': DP_URL}
    puzzle_page = session.post(DP_URL, query, headers=header).content
    with open('dump/dumpDP.html', 'w') as dump:
        dump.write(puzzle_page.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('NP', puzzle_page)):
        return True
    return False

def getTombola(session):
    '''
    Needs soup.
    '''
    header = {'Referer': 'http://www.neopets.com/island/tombola.phtml'}
    tombolaPage = session.post(tombolaURL, headers=header).content
    with open('dump/dumpTombola.html', 'w') as dump:
        dump.write(tombolaPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('win', tombolaPage)):
        return True
    return False

def getColtzan(session):
    '''
    Needs soup.
    '''
    query = {'type': 'approach'}
    coltzanPage = session.post(coltzanURL, query).content
    with open('dump/dumpColtzan.html', 'w') as dump:
        dump.write(coltzanPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('young', coltzanURL)):
        return True
    return False

def getToys(session):
    query = {'go': 1}
    toyPage = session.post(toyURL, query).content
    with open('dump/dumpToy.html', 'w') as dump:
        dump.write(toyPage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)', toyPage)
    if(winnings):
        return winnings[0]
    return False

def getTomb(session):
    tombPage = session.post(tombURL).content
    with open('dump/dumpTomb.html', 'w') as dump:
        dump.write(tombPage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', tombPage)
    if(winnings):
        return winnings[0]
    if(re.findall('laughing', tombPage)):
        return 'Jackpot'
    return False

def getKrawken(session):
    krawkenPage = session.get(krawkenURL).content
    if(re.findall('more, huh?', krawkenPage)):
        print 'Krawken on cooldown.'
        return False
    ck = re.findall('action" type="hidden" value="([a-f\d]+)"', krawkenPage)
    query = {'action' : ck}
    krawkenPage = session.post(krawkenURL, query).content
    with open('dump/dumpKrawken.html', 'w') as dump:
        dump.write(krawkenPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('prize-item-name">([\w\d ,\._]+)<', krawkenPage)):
        return re.findall('prize-item-name">([\w\d ,\._]+)<', krawkenPage)[0]
    return False

def getObsidian(session):
    obsidianPage = session.get(obsidianURL).content
    with open('dump/dumpObsidian.html', 'w') as dump:
        dump.write(obsidianPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('shakes', obsidianPage)):
        return False
    return 'Obsidian get'

def getFruit(session):
    '''
    Works, win condition untested.
    '''
    fruitPage = session.get(fruitURL).content
    ck = re.findall('ck" value="([a-f\d]+)', fruitPage)
    if(ck):
        query = {'spin':1, 'ck':ck}
    else:
        return False
    fruitPage = session.post(fruitURL, query).content
    with open('dump/dumpFruit.html', 'w') as dump:
        dump.write(fruitPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('this is not a win', fruitURL)):
        return 'nothing'
    winnings = re.findall('you won a <b>([\d\w ]+)</b>', fruitPage)
    if(len(winnings)):
        return winnings[0]
    return False

def getApple(session):
    #query = {'bobbing': 1}
    applePage = session.get(appleURL).content
    with open('dump/dumpApple.html', 'w') as dump:
        dump.write(applePage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('<b>inventory</b>', applePage)):
        winnings = re.findall('80\'><br><b>([\d\w ,\.]+)</b></center>', applePage)
        if winnings:
            return winnings[0]
        return True
    return False

def getPlushie(session):
    query = {'talkto':1}
    plushiePage = session.post(plushieURL, query).content
    with open('dump/dumpPlushie.html', 'w') as dump:
        dump.write(plushiePage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', plushiePage)
    if(winnings):
        return winnings[0]
    if(re.findall('!</b>', plushiePage)):
        return re.findall('<b>([\d\w ,_\.]+)</b>!</div>', plushiePage)
    return False

def getFish(session):
    query = {'go_fish':1}
    fishingPage = session.post(fishingURL, query).content
    with open('dump/dumpFishing.html', 'w') as dump:
        dump.write(fishingPage.encode('ascii', 'xmlcharrefreplace'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', fishingPage)
    if(winnings):
        return winnings[0]
    return 'unknown state'

def getSlorg(session):
    query = {'slorg_payout': 'yes'}
    slorgPage = session.post(slorgURL, query).content
    with open('dump/dumpSlorg.html', 'w') as dump:
        dump.write(slorgPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('rich', slorgPage)):
        return re.findall('<strong>([\d\.,]+) N', slorgPage)[0]
    return False

def getInterest(session):
    query = {'type':'interest'}
    session.post(bankPostURL, query)
    bankPage = session.get(bankGetURL).content
    with open('dump/dumpBank.html', 'w') as dump:
        dump.write(bankPage.encode('ascii', 'xmlcharrefreplace'))
    interest = re.findall('([\d, ]+)NP', bankPage)
    if(re.findall('You have', bankPage)):
        return interest[0]
    return False

def getJelly(session):
    query = {'type':'get_jelly'}
    jellyPage = session.post(jellyURL, query).content
    with open('dump/dumpJelly.html', 'w') as dump:
        dump.write(jellyPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('You take some', jellyPage)):
        return re.findall('items/([\d\w, _]+)', jellyPage)[0]
    if(re.findall('eaten!!!', jellyPage)):
        print 'Jelly has been eaten.'
        return False
    return False

def getOmelette(session):
    query = {'type':'get_omelette'}
    omelettePage = session.post(omeletteURL, query).content
    with open('dump/dumpOmelette.html', 'w') as dump:
        dump.write(omelettePage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('(Sabre-X)|(Gone!!!)', omelettePage)):
        print 'Aready taken'
        return False
    if(re.findall('... and', omelettePage)):
        return re.findall('items/([\d\w, _]+)\.gif\' width=80',
                omelettePage)[0]
    return False

def getLunar(session):
    lunarPage = session.get(lunarGetURL).content
    angle = int(re.findall('Kreludor=([\d\.]+)', lunarPage)[0])
    answer = int(round(angle/22.5)%16)
    if answer > 7:
        answer -= 8
    else:
        answer += 8
    answer = {'submitted':'true','phase_choice':answer}
    lunarPage = session.post(lunarPostURL, answer).content
    with open('dump/dumpLunar.html', 'w') as dump:
        dump.write(lunarPage.encode('ascii', 'xmlcharrefreplace'))
    if(re.findall('correct', lunarPage)):
        return re.findall('items/([\w\d _,]+)\.gif', lunarPage)[0]
    return False

def login(login_header={}):
    s = requests.session()
    login = {'username':raw_input('Username: '),'password':getpass.getpass()}
    response = s.post('http://www.neopets.com/login.phtml', login,
            headers=login_header)
    if(re.findall(login['username'], response.content)):
        print 'Login successful as:', s.cookies['neoremember']
        return s
    print 'Unsuccessful login.'
    return s

if __name__ == '__main__':
    print 'Herpaderp'


