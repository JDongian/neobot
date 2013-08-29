import sys
import time
from bs4 import BeautifulSoup
import re
import getpass
import requests
import random

shopwizard_URL = 'http://www.neopets.com/market.phtml'


def login(cred={}, login_header={}):
    s = requests.session()
    login_header['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    login_header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    if not cred:
        cred = {'username':raw_input('Username: '),'password':getpass.getpass()}
    response = s.post('http://www.neopets.com/login.phtml', cred,
            headers=login_header)
    return s

def get_results(item_name, session, header={}):
    query = {
        'type': 'process_wizard',
        'feedset': 0,
        'shopwizard': item_name,
        'table': 'shop',
        'criteria': 'exact',
        'min_price': 0,
        'max_price': 99999
    }
    header['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    header['Referer'] = 'http://www.neopets.com/market.phtml?type=wizard'
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    page = session.post(shopwizard_URL, query, headers=header).content
    return zip([int(price) for price in
        re.findall('buy_cost_neopoints=(\d+)', page)],
        re.findall('owner=([^&]+)&', page),
        re.findall('/browseshop[^"]+', page))

def _buy_item_from_owner(url, session, header={}):
    header['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'
    header['Referer'] = 'http://www.neopets.com/market.phtml'
    header['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    shop = session.post('http://www.neopets.com'+url, headers=header).content
    purchase_url = 'http://www.neopets.com/'+re.findall('buy_item[^"]+', shop)[0]
    header['Referer'] = 'http://www.neopets.com'+url
    result = session.get(purchase_url, headers=header)
    return result.content

#def get_price(html_content)

if __name__=='__main__':
    cred = {}
    with open('LOGIN', 'r') as c:
        cred['username'] = c.readline()[:-1]
        cred['password'] = c.readline()[:-1]
        print cred
        s = login(cred)
    command = ''
    while 1:
        item = raw_input('Item name: ')
        lowest = [99999, '', '']
        for i in range(32):
            result = sorted(get_results(item, s), key=lambda r:
                    r[0])[0]
            if result[0] <= lowest[0]:
                lowest = result
            print '\r%d NP at %s.' % lowest[:-1], '                           ',
            sys.stdout.flush()
            if lowest[0] == 1:
                break
            time.sleep(0.2+random.random())
        print ''
        command = raw_input('Buy or retry? ')
        if command == 'buy':
            if _buy_item_from_owner(lowest[2], s)[:5] == '<cent':
                print 'Inventory Full.'
            else:
                print 'Item purchased for %d NP from %s.' % lowest[:-1]
        elif command == 'retry':
            print 'Type it yourself.'

