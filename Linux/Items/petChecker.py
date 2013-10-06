import random
import time
import re
import requests

pet_url = 'http://www.neopets.com/reg/page4.phtml'


def login(cred={}, login_header={}):
    s = requests.session()
    if not cred:
        cred = {'username':raw_input('Username: '),'password':getpass.getpass()}
    response = s.post('http://www.neopets.com/login.phtml', cred,
            headers=login_header)
    return s

def check(s):
    results = 0
    pet_page = s.get(pet_url).content
    try:
        results = re.findall("Available Limited Edition Neopets:</div>([^@]*)<div id='colour_label' style='color: green;", pet_page)[0]
    except:
        print 'Error at %d:%s' % (int(time.localtime().tm_hour),
                str(int(time.localtime().tm_min)).zfill(2))
    if len(results) != 168:
        print '======\n%s\n======\n\nat %d:%s' % (results,
                int(time.localtime().tm_hour),
                str(int(time.localtime().tm_min)).zfill(2))
    return results

if __name__=='__main__':
    cred = {}
    with open('LOGIN', 'r') as c:
        cred['username'] = c.readline()[:-1]
        cred['password'] = c.readline()[:-1]
        s = login(cred)
    print 'Logged in with session: %s' % str(s)
    curr_time = time.localtime()
    while True:
        if time.localtime().tm_hour == curr_time.tm_hour and\
           time.localtime().tm_yday != curr_time.tm_yday:
            break
        check(login(cred))
        time.sleep(60*60*24*(1-random.random()*0.05))
    print 'Done.'

