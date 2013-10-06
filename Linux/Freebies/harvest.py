import DailyFreebies
from re import split

default_header = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130626 Firefox/17.0 Iceweasel/17.0.7',
    'Accept-Language': 'en-US,en;q=0.5',
    'Host': 'www.neopets.com',
}

if __name__ == '__main__':
    login_header = default_header
    login_header['Referer'] = 'http://www.neopets.com/login/index.phtml'
    login = True
    with open('LOGIN', 'r') as credentials:
        while login:
            login = credentials.readline()[:-1]
            if login == '':
                continue
            login = login.split(' ')
            s = DailyFreebies.login(username=login[0],
                                    password=login[1],
                                    header=login_header)
            for f in DailyFreebies.__dict__.keys():
                if f[:3] == 'get' and f[3] != 'p':
                    freebie = getattr(DailyFreebies, f)
                    print f, '\t', freebie(s)
