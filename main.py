import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime, date
from dotenv import load_dotenv
import os
import logging
import sys
import edip
import urnebesna_tragedija

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)

load_dotenv()

global_email_content = ''

def append_to_global(s):
    global global_email_content
    global_email_content += s

def clear_global():
    global global_email_content
    global_email_content = ''

def send_email(subject, content):
    email_address = os.getenv('EMAIL_SENDER')
    email_password = os.getenv('EMAIL_SENDER_PASSWORD')
    msg = EmailMessage()
    msg['Subject'] = subject + " - " + datetime.now().strftime('%b')
    msg['From'] = email_address
    msg['To'] = os.getenv('EMAIL_RECEIVER')
    msg.set_content(content)
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

def pozoriste_job():
    logging.info('| Running Pozoriste job')
    if(datetime.now().minute >= 0 and datetime.now().minute < 3): # check first 3 minutes of the hour
        append_to_global(edip.check_dates())
        append_to_global(urnebesna_tragedija.check_dates())
    
    if(len(global_email_content) > 0):
        logging.info('-> Pozoriste email sending...')
        send_email('Pozoriste - datumi', global_email_content)
        logging.info('-> Pozoriste email sent!')
    else:
        logging.info('-> Pozoriste email not sent (no dates)')
    clear_global()

pozoriste_job()

def check_Arena_Today():
    logging.info('| Running Arena job')
    URL = 'https://starkarena.co.rs/lat/dogadjaji/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    try:
        page = requests.get(URL, headers=headers)
    except Exception as e:
        logging.error('!!! Exception: ' + str(e))
        send_email('Arena danas!', 'Error getting Arena page')
        return
    soup = BeautifulSoup(page.content, 'html.parser')

    head_info = soup.find('div', 'head_info')

    event_date = head_info.find('p', 'datetime').text.strip()[0:2]
    if(event_date.startswith('0')):
        event_date = event_date[1]

    event_name = head_info.find('h2').text.strip()

    event_description = head_info.find_all('p')[1].text.strip()

    if(int(event_date) == date.today().day and datetime.now().hour == 12 and datetime.now().minute == 0):
        logging.info('-> Arena email sending...')
        send_email('Arena danas!', '{}\n{}'.format(event_name, event_description))
        logging.info('-> Arena email sent!')
    else:
        logging.info('-> Arena email not sent (no event today)')

check_Arena_Today()
