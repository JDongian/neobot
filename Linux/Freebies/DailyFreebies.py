import operator
import random
import re
import requests
import json
import getpass
from bs4 import BeautifulSoup
import datetime
from pprint import pprint
import time

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
potato_URL = 'http://www.neopets.com/medieval/potatocounter.phtml'
hideURL = 'http://www.neopets.com/games/process_hideandseek.phtml'
DP_URL = 'http://www.neopets.com/community/index.phtml'
crossword_URL = 'http://www.neopets.com/games/crossword/crossword.phtml'
answers_URL = 'http://www.tdnforums.com/index.php?/rss/forums/3-faerie-crossword-answers-from-tdn/'

def hide(session):
    """Hide and seek.
    Needs testing.
    """
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
    """Guess the marrow.
    Needs avail. checking
    """
    query = {'guess':642}
    #query = {'guess':int(raw_input('Marrow weight? '))}
    marrowPage = session.post(marrowURL, query).content
    if(re.findall('WRONG!', marrowPage)):
        return False
    return True


"""
Helper functions
"""

def login(username=None, password=None, header={}):
    s = requests.session()
    if username and password:
        user = {'username': username,
                 'password': password}
        print "Logging in as %s using local file" % username
    else:
        print "No LOGIN file found."
        user = {'username':raw_input('Username: '),
                 'password':getpass.getpass()}
    response = s.post('http://www.neopets.com/login.phtml', params=user,
                      headers=header)
    if response.status_code != 200:
        print 'Unsuccessful login.'
        quit()
    return s

def _get_DP():
    """Daily puzzle game.
    """
    answer_page = requests.get(answers_URL).content
    answer = re.findall('</strong> ([A-Z0-9].*?)<br', answer_page)
    date = re.findall('<title>.*?(\d+).*?</title', answer_page)
    if answer and date:
        return answer[0], date[0]
    else:
        print 'error on fetching answers'
        return False

def _get_crossword():
    """Faerie crossword solver.
    """
    answer_page = requests.get(answers_URL).content
    across = re.findall('Across:</strong><br />\s*([^`]*?)\s*<td', answer_page)
    down = re.findall('Down:</strong><br />\s*([^`]*?)\s*<td', answer_page)
    if across and down:
        return [re.findall('(\d+)\.\s+(.*?)<br', across[0]),
                re.findall('(\d+)\.\s+(.*?)<br', down[0])]
    else:
        return False

"""
(MOSTLY) FINISHED METHODS
"""

def get_potato(session):
    """Potato counter 1.
    """
    for i in xrange(3):
        potato_page = session.get(potato_URL).content
        soup = BeautifulSoup(potato_page)
        potato_table = soup.find_all('table', align='center')
        if potato_table:
            potato_table = potato_table[0]
        else:
            print 'Done for the day.'
            return False
        potato_count = len(re.findall('gif', str(potato_table)))
        form = {'type': 'guess', 'guess': potato_count}
        time.sleep((potato_count/10)*(1+random.random()))
        potato_page = session.post(potato_URL, form).content
    with open('dump/dumpPotato.html', 'w') as dump:
        dump.write(''.join([c for c in potato_page if ord(c) < 128]))
    return True

def get_crossword(session, header={}):
    """Faerie crossword solver.
    """
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
                    if crossword_model[row+1][col] != '  ':
                        crossword_positions[current+u' down'] =  col, row
                if col < len(crossword_model[0])-1:
                    if crossword_model[row][col+1] != '  ':
                        crossword_positions[current+u' across'] = col, row
    #pprint(crossword_positions)

    header['Referer'] = 'http://www.neopets.com/games/crossword/crossword.phtml'
    for ans, direction in sorted(answers, key=lambda x: int(x[0][0])):
        query = {
            'x_word': ans[1],
            'showclue': ans[0]+' '+direction,
            'x_clue_row': crossword_positions[ans[0].zfill(2)+' '+direction][1]+1,
            'x_clue_col': crossword_positions[ans[0].zfill(2)+' '+direction][0]+1,
            'x_clue_dir': (lambda f: {'across': 1, 'down': 2}[f])(direction)
        }
        #print query
        crossword_page = session.post(crossword_URL, query, headers=header).content
        with open('dump/dumpCrosswords.html', 'w') as dump:
            pass#dump.write(crossword_page.decode('utf-8').encode('ascii', 'ignore'))
    if 1:
        return True

def get_puzzle(session):
    """Daily puzzle solver.
    """
    answer, neodate = _get_DP()
    question_page = requests.get(DP_URL).content
    with open('dump/dumpDP.html', 'w') as dump:
        dump.write(question_page.decode('utf-8').encode('ascii', 'ignore'))
    result = re.findall("'(\d)'>.*?"+answer+'.*?</option>',
            question_page, re.IGNORECASE)
    print answer
    print result
    answer = result[0]
    query = {
        'trivia_date': str(datetime.date.today())[:-2]+neodate.zfill(2),
        'trivia_response': int(answer)+1,
        'submit': 'Submit'
    }
    header = {'Referer': DP_URL}
    #print query, header
    puzzle_page = session.post(DP_URL, query, headers=header).content
    with open('dump/dumpDP.html', 'w') as dump:
        dump.write(puzzle_page.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('NP', puzzle_page)):
        return True
    return False

def get_tombola(session):
    """Tombola player.
    Needs soup.
    """
    header = {'Referer': 'http://www.neopets.com/island/tombola.phtml'}
    tombolaPage = session.post(tombolaURL, headers=header).content
    with open('dump/dumpTombola.html', 'w') as dump:
        pass#dump.write(tombolaPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('win', tombolaPage)):
        return True
    return False

def get_coltzan(session):
    """Coltzan's shrine.
    Needs soup.
    """
    query = {'type': 'approach'}
    coltzanPage = session.post(coltzanURL, query).content
    with open('dump/dumpColtzan.html', 'w') as dump:
        pass#dump.write(coltzanPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('young', coltzanURL)):
        return 'young'
    return True

def get_toys(session):
    """Toy chest.
    """
    query = {'go': 1}
    toyPage = session.post(toyURL, query).content
    with open('dump/dumpToy.html', 'w') as dump:
        pass#dump.write(toyPage.decode('utf-8').encode('ascii', 'ignore'))
    winnings = re.findall('items/([\d\w, _]+)', toyPage)
    if(winnings):
        return winnings[0]
    return False

def get_tomb(session):
    """Geritipuku tomb.
    """
    tombPage = session.post(tombURL).content
    with open('dump/dumpTomb.html', 'w') as dump:
        pass#dump.write(tombPage.decode('utf-8').encode('ascii', 'ignore'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', tombPage)
    if(winnings):
        return winnings[0]
    if(re.findall('laughing', tombPage)):
        return 'Jackpot'
    return False

def get_krawken(session):
    """Anchor management.
    """
    krawkenPage = session.get(krawkenURL).content
    if(re.findall('more, huh?', krawkenPage)):
        print 'Krawken on cooldown.'
        return False
    ck = re.findall('action" type="hidden" value="([a-f\d]+)"', krawkenPage)
    query = {'action' : ck}
    krawkenPage = session.post(krawkenURL, query).content
    with open('dump/dumpKrawken.html', 'w') as dump:
        pass#dump.write(krawkenPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('prize-item-name">([\w\d ,\._]+)<', krawkenPage)):
        return re.findall('prize-item-name">([\w\d ,\._]+)<', krawkenPage)[0]
    return False

def get_obsidian(session):
    """Obsidian quarry.
    """
    obsidianPage = session.get(obsidianURL).content
    with open('dump/dumpObsidian.html', 'w') as dump:
        pass#dump.write(obsidianPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('shakes', obsidianPage)):
        return False
    return 'Obsidian get'

def get_fruit(session):
    """Fruit machine.
    Works, win condition untested
    """
    fruitPage = session.get(fruitURL).content
    ck = re.findall('ck" value="([a-f\d]+)', fruitPage)
    if(ck):
        query = {'spin':1, 'ck':ck}
    else:
        return False
    fruitPage = session.post(fruitURL, query).content
    with open('dump/dumpFruit.html', 'w') as dump:
        pass#dump.write(fruitPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('this is not a win', fruitURL)):
        return 'nothing'
    winnings = re.findall('you won a <b>([\d\w ]+)</b>', fruitPage)
    if(len(winnings)):
        return winnings[0]
    return True

def get_apple(session):
    """Apple bobbing.
    """
    #query = {'bobbing': 1}
    applePage = session.get(appleURL).content
    with open('dump/dumpApple.html', 'w') as dump:
        pass#dump.write(applePage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('<b>inventory</b>', applePage)):
        winnings = re.findall('80\'><br><b>([\d\w ,\.]+)</b></center>', applePage)
        if winnings:
            return winnings[0]
        return True
    return False

def get_plushie(session):
    """The magical discarded blue grundo plushie thing.
    """
    import codecs
    query = {'talkto':1}
    plushiePage = session.post(plushieURL, query).content
    with open('dump/dumpPlushie.html', 'w') as dump:
        #plushiePage = unicode(plushiePage.strip(codecs.BOM_UTF8), 'utf-8')
        pass#dump.write(plushiePage)#.decode('utf-8').encode('ascii', 'ignore'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', plushiePage)
    if(winnings):
        return winnings[0]
    if(re.findall('!</b>', plushiePage)):
        return re.findall('<b>([\d\w ,_\.]+)</b>!</div>', plushiePage)
    return False

def get_fish(session):
    """Underground fishing.
    """
    query = {'go_fish':1}
    fishingPage = session.post(fishingURL, query).content
    with open('dump/dumpFishing.html', 'w') as dump:
        pass#dump.write(fishingPage.decode('utf-8').encode('ascii', 'ignore'))
    winnings = re.findall('items/([\d\w, _]+)\.gif', fishingPage)
    if(winnings):
        return winnings[0]
    return 'unknown state'

def get_slorg(session):
    """Rich slorg.
    """
    query = {'slorg_payout': 'yes'}
    slorgPage = session.post(slorgURL, query).content
    with open('dump/dumpSlorg.html', 'w') as dump:
        pass#dump.write(slorgPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('rich', slorgPage)):
        return re.findall('<strong>([\d\.,]+) N', slorgPage)[0]
    return False

def get_interest(session):
    """Bank interest collector.
    """
    query = {'type':'interest'}
    session.post(bankPostURL, query)
    bankPage = session.get(bankGetURL).content
    with open('dump/dumpBank.html', 'w') as dump:
        pass#dump.write(bankPage.decode('utf-8').encode('ascii', 'ignore'))
    interest = re.findall('([\d, ]+)NP', bankPage)
    if(re.findall('You have', bankPage)):
        return interest[0]
    return False

def get_jelly(session):
    """Free jelly.
    """
    query = {'type':'get_jelly'}
    jellyPage = session.post(jellyURL, query).content
    with open('dump/dumpJelly.html', 'w') as dump:
        pass#dump.write(jellyPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('You take some', jellyPage)):
        return re.findall('items/([\d\w, _]+)', jellyPage)[0]
    if(re.findall('eaten!!!', jellyPage)):
        print 'Jelly has been eaten.'
        return False
    return False

def get_omelette(session):
    """Tyrannian omelette.
    """
    query = {'type':'get_omelette'}
    omelettePage = session.post(omeletteURL, query).content
    with open('dump/dumpOmelette.html', 'w') as dump:
        pass#dump.write(omelettePage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('(Sabre-X)|(Gone!!!)', omelettePage)):
        print 'Aready taken'
        return False
    if(re.findall('items/([\d\w, _]+)\.gif\' width=80', omelettePage)):
        return re.findall('items/([\d\w, _]+)\.gif\' width=80',
                omelettePage)[0]
    return False

def get_lunar(session):
    """Lunar quiz.
    """
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
        pass#dump.write(lunarPage.decode('utf-8').encode('ascii', 'ignore'))
    if(re.findall('correct', lunarPage)):
        return re.findall('items/([\w\d _,]+)\.gif', lunarPage)[0]
    return False

if __name__ == '__main__':
    print 'Herpaderp'


