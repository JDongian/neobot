import random
import time
import re
import requests

pool_URL = 'http://www.neopets.com/magma/pool.phtml'


def login(cred={}, login_header={}):
    s = requests.session()
    if not cred:
        cred = {'username':raw_input('Username: '),'password':getpass.getpass()}
    response = s.post('http://www.neopets.com/login.phtml', cred,
            headers=login_header)
    return s

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
        time.sleep(60*(9+random.random()*5))
        if(random.choice((False, True, True))):
            s = login(cred)
        pool_page = s.get(pool_URL).content
        try:
            result = re.findall('http://images\.neopets\.com/magma/pool/guard_(.*)\.jpg',
                pool_page)[0]
        except:
            print 'Error at %d:%s' % (int(time.localtime().tm_hour),
                    str(int(time.localtime().tm_min)).zfill(2))
        if result != 'rejected':
            print 'Guard: %s at %d:%s' % (result,
                    int(time.localtime().tm_hour),
                    str(int(time.localtime().tm_min)).zfill(2))
    print 'Done.'
