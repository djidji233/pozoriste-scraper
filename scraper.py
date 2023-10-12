import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime, date

def send_email(subject, content):
    # set your email and password
    # please use App Password
    email_address = "kassad.tips@gmail.com"
    email_password = "orntdmglacxlbskm"
    # create email
    msg = EmailMessage()
    msg['Subject'] = subject + " - " + datetime.now().strftime('%b')
    msg['From'] = email_address
    msg['To'] = "djolezile@gmail.com"
    msg.set_content(content)
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
    # return content

def check_dates_Voz():
    URL = 'https://zvezdarateatar.rs/predstava/voz/21/#'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    dates = soup.find('span', class_='predstava-dates').get_text().strip()

    if(dates):
        return send_email("Voz - Zvezdara Teatar", dates)
    else:
        return send_email('Error getting dates')

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
        return send_email("Edip - JDP", content)
    else:
        return send_email('Error getting dates')
    
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
        return send_email("Urnebesna Tragedija - Narodno", content)
    else:
        return send_email('Error getting dates')
     

def job():
    if(date.today().day > 27 or date.today().day < 4):
        check_dates_Voz() 
        check_dates_Edip()
        check_dates_UrnebesnaTragedija()

job()