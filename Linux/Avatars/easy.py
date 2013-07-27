import re
import requests
import getpass

def easy(session, header={}):
    with open('links.txt') as links:
        for l in links:
            print l
            try:
                session.get('http://'+l[:-1], headers=header)
            except:
                print 'Failed on %s' % l[4:-1]
                pass

def login(login_header={}):
    s = requests.session()
    login = {'username': raw_input('Username: '),'password': getpass.getpass()}
    response = s.post('http://www.neopets.com/login.phtml', login,
            headers=login_header)
    return s

if __name__ == '__main__':
    easy(login())
