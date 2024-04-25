import requests
from bs4 import BeautifulSoup
from datetime import datetime, date

def run(url, name):
    content = ''
    URL = url
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    form_data = {
        'q': '1',
        'godina': date.today().year,
        'mesec': date.today().month + 1,
        'sdsp': '1',
        'trazi': name,
        'user_tipid': '',
        'sap': '1',
        'ss': '0',
        'tip_prikaza': '0',
    }
    try:
        results = requests.post(URL, headers=headers, data=form_data).json()
    except:
        print('{} - Error getting dates\n'.format(name))
        return ''
        
    if(len(results) == 0):
        return ''
    else:
        for r in results:
            datum = r['datum']
            vreme = r['vreme'][0:5]
            datum_formatted = datetime.strptime(datum, '%Y-%m-%d').strftime('%d. %b')
            content += "{} - {}\n".format(datum_formatted, vreme)
            
    content += ('\n')
    
    return content