import requests
from bs4 import BeautifulSoup

import smtplib
from email.message import EmailMessage

from datetime import datetime

def check_dates():
    URL = 'https://zvezdarateatar.rs/predstava/voz/21/#'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    predstava_dates = soup.find('span', class_='predstava-dates').get_text().strip()
    # print(predstava_dates)

    if(predstava_dates):
        send_email(predstava_dates)
    else:
        send_email('error getting dates')

def send_email(message):
    # set your email and password
    # please use App Password
    email_address = "kassad.tips@gmail.com"
    email_password = "orntdmglacxlbskm"
    # create email
    msg = EmailMessage()
    msg['Subject'] = "Voz - Zvezdara Teatar - " + datetime.now().strftime('%b')
    msg['From'] = email_address
    msg['To'] = "djolezile@gmail.com"
    msg.set_content(message)
    # send email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
    # print('Email sent!')

check_dates()