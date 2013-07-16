import pprint
import operator
import requests
from bs4 import BeautifulSoup
import re

crossword_URL = 'http://www.neopets.com/games/crossword/crossword.phtml'
answers_URL = 'http://www.tdnforums.com/index.php?/rss/forums/3-faerie-crossword-answers-from-tdn/'

crossword = 0
#crossword = requests.post(crossword_URL).content
with open('/home/joshua/Documents/git/tmp/neobot/crossword.html', 'r') as crossword_page:
    crossword = crossword_page.read()


def _get_crossword():
    answer_page = requests.get(answers_URL).content
    across = re.findall('Across:</strong><br />\n([^~]*?)<td', answer_page)
    down = re.findall('Down:</strong><br />\n([^~]*?)<td', answer_page)
    if across and down:
        return (re.findall('([0-9]+)\. (.*?)<br', across[0]),
                re.findall('([0-9]+)\. (.*?)<br', down[0]))
    else:
        return False

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
for r in crossword_model:
    pprint.pprint(r)
answers = _get_crossword()
answers = sorted(answers[0]+answers[1], key=lambda f: int(f[0]))
for i, a in answers[:3]:
    direction = 'across'
    query = {
        'x_word': a,
        'showclue': i+' '+direction,
        'x_clue_row': 4,
        'x_clue_col': 4,
        'x_clue_dir': (lambda f: {'across': 1, 'down': 2}[f])(direction)
    }
    pprint.pprint(query)
    print ''
for y in xrange(len(crossword_model)):
    for x in xrange(len(crossword_model[0])):
        print crossword_model[x][y]


