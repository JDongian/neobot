from bs4 import BeautifulSoup
import reqests

default_session = 0
def get_results(item_name, session=default_session):
    query = {
        'type': 'process_wizard',
        'feedset': 0,
        'shopwizard': itemName,
        'table': 'shop',
        'criteria': exact,
        'min_price': 0,
        'max_price': 99999
    }
    page = session.post(shopWizardURL, query)
    return page.content

def get_price(html_content)

