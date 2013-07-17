import pprint
import operator
import requests
from bs4 import BeautifulSoup
import re
from itertools import chain

crossword_URL = 'http://www.neopets.com/games/crossword/crossword.phtml'
answers_URL = 'http://www.tdnforums.com/index.php?/rss/forums/3-faerie-crossword-answers-from-tdn/'

crossword = 0
#crossword = requests.post(crossword_URL).content
with open('/home/joshua/Documents/git/tmp/neobot/crossword.html', 'r') as crossword_page:
    crossword = crossword_page.read()


def _get_crossword():
    answer_page = requests.get(answers_URL).content
    across = re.findall('Across:</strong><br />\n([^`]*?)<td', answer_page)
    down = re.findall('Down:</strong><br />\n([^`]*?)<td', answer_page)
    if across and down:
        return [re.findall('(\d+)\.\s+(.*?)<br', across[0]),
                re.findall('(\d+)\.\s+(.*?)<br', down[0])]
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
answers = zip(answers[0], ['across']*len(answers[0]))+zip(answers[1], ['down']*len(answers[0]))
#answers = sorted(answers[0]+answers[1], key=lambda f: int(f[0]))

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
pprint.pprint(crossword_positions)

for ans, direction in sorted(answers, key=lambda x: int(x[0][0])):
    query = {
        'x_word': ans[1],
        'showclue': ans[0]+' '+direction,
        'x_clue_row': crossword_positions[ans[0].zfill(2)+' '+direction][1],
        'x_clue_col': crossword_positions[ans[0].zfill(2)+' '+direction][0],
        'x_clue_dir': (lambda f: {'across': 1, 'down': 2}[f])(direction)
    }
    pprint.pprint(query)
    print ''


