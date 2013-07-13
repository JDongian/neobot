import requests
import getpass









def login():
    s = requests.session()
    login = {'username':raw_input('Username:'),'password':getpass.getpass()}
    s.post('http://www.neopets.com/login.phtml', login).content
    if('neoremember' in s.cookies.keys()):
        return s
    print 'Login error.'
    return False













 re.findall('openwin\((\d+)\).*items/([\d\w_ ,\.]+)\.gif".*</a><br>([\d\w\._, ]+)<hr', inventoryPage)
