import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime, date
import time

global_email_content = ''

def append_to_global(s):
    global global_email_content
    global_email_content += s

def clear_global():
    global global_email_content
    global_email_content = ''

def send_email(subject, content):
    email_address = "kassad.tips@gmail.com"
    email_password = "orntdmglacxlbskm" # app password
    msg = EmailMessage()
    msg['Subject'] = subject + " - " + datetime.now().strftime('%b')
    msg['From'] = email_address
    msg['To'] = "djolezile@gmail.com"
    msg.set_content(content)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

def check_dates_Voz():
    URL = 'https://zvezdarateatar.rs/predstava/voz/21/#'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    dates = soup.find('span', class_='predstava-dates').get_text().strip()

    if(dates):
        # return send_email("Voz - Zvezdara Teatar", dates)
        append_to_global('Voz - Zvezdara Teatar:\n')
        append_to_global(dates + '\n')
        append_to_global('\n')
    else:
        # return send_email('Error getting dates')
        append_to_global('Voz - Zvezdara Teatar:\n')
        append_to_global('Error getting dates\n')
        append_to_global('\n')

def check_dates_Edip():
    URL = 'https://www.jdp.rs/performance/edip/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    dates = soup.find_all('div', 'calendar__item-date js-date')
    content = ''
    for date_div in dates:
         day_div = date_div.find('div', 'day')
         day = day_div.find('strong').text
         month = day_div.find('span').text
         content += day+' '+month+'\n'

    if(dates):
        # return send_email("Edip - JDP", content)
        append_to_global('Edip - JDP:\n')
        append_to_global(content + '\n')
    
    else:
        # return send_email('Error getting dates')
        append_to_global('Edip - JDP:\n')
        append_to_global('Error getting dates\n')
    
def check_dates_UrnebesnaTragedija():
    URL = 'https://www.narodnopozoriste.rs/lat/predstave/urnebesna-tragedija'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    dates = soup.find_all('div', 'repertoarwide-entry-date')
    content = ''
    for date_div in dates:
        day = date_div.contents[1].strip()
        month = date_div.find('span', 'mesec').text
        content += day+' '+month+'\n'

    if(dates):
        # return send_email("Urnebesna Tragedija - Narodno", content)
        append_to_global('Urnebesna Tragedija - Narodno:\n')
        append_to_global(content + '\n')
    else:
        # return send_email('Error getting dates')
        append_to_global('Urnebesna Tragedija - Narodno:\n')
        append_to_global('Error getting dates\n')
     

def job():
    if(date.today().day > 20 and date.today().day < 26):
        check_dates_Voz() 
        check_dates_Edip()
        check_dates_UrnebesnaTragedija()
        time.sleep(8) # in case scraping takes some time
        send_email('Pozoriste - datumi', global_email_content)
        clear_global()

job()

def check_Arena_Today():
    URL = 'https://starkarena.co.rs/lat/dogadjaji/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    head_info = soup.find('div', 'head_info')

    event_date = head_info.find('p', 'datetime').text.strip()[0:2]
    if(event_date.startswith('0')):
        event_date = event_date[1]

    event_name = head_info.find('h2').text.strip()

    event_description = head_info.find_all('p')[1].text.strip()

    if(int(event_date) == date.today().day):
        send_email('ARENA DANAS', '{}\n{}'.format(event_name, event_description))

check_Arena_Today()