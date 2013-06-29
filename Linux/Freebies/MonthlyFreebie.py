import requests
import getpass

freebieURL = 'http://www.neopets.com/freebies/index.phtml'

def redeem(session):
    session.get(freebieURL)

if __name__ == '__main__':
    s = requests.session()
    login = {'username':raw_input('Username: '),'password':getpass.getpass()}
    s.post('http://www.neopets.com/login.phtml', login)
    redeem(s)

