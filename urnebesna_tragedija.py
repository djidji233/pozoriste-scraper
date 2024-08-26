import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import logging

def check_dates():
    logging.info('* Checking dates for URNEBESNA TRAGEDIJA')
    content = ''
    content += ('Urnebesna Tragedija - Narodno:\n')
    URL = 'https://www.narodnopozoriste.rs/lat/predstave/urnebesna-tragedija'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    try:
        page = requests.get(URL, headers=headers)
    except Exception as e:
        logging.error('!!! Exception: ' + str(e))
        content += ('Error getting dates\n')
        return content
    soup = BeautifulSoup(page.content, 'html.parser')
    dates = soup.find_all('div', 'repertoarwide-entry-date')
    current_content = ''
    for date_div in dates:
        day = date_div.contents[1].strip()
        month = date_div.find('span', 'mesec').text
        current_content += day+' '+month+'\n'

    if(dates):
        content += (current_content)

    content += ('\n')
    
    if(len(content) > len('Urnebesna Tragedija - Narodno:\n\n')):
        return content
    else:
        return ''