import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime, date
from dotenv import load_dotenv
import os
import voz
import milutin
import edip
import ljubavno_pismo
import urnebesna_tragedija

'''
    TODO:
    - add listener that fetches every minute during the selected days of month
        - railway cron supports something like this: (TESTING)
            * 10-11 21,22,23,24,25 * * 
            (Every minute, between 10:00 and 11:59, on day 21, 22, 23, 24, and 25 of the month)
'''
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
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)

def pozoriste_job():
    if(datetime.now().minute >= 0 and datetime.now().minute < 3):
        # append_to_global(voz.check_dates()) # KUPLJENO
        # append_to_global(milutin.check_dates()) # KUPLJENO
        append_to_global(ljubavno_pismo.check_dates())
        append_to_global(edip.check_dates())
        # append_to_global(urnebesna_tragedija.check_dates()) # not available any more ?
        
        if(len(global_email_content) > 0):
            # print('From:', os.getenv('EMAIL_SENDER'))
            # print('To:', os.getenv('EMAIL_RECEIVER'))
            # print('Body:\n' + global_email_content)
            send_email('Pozoriste - datumi', global_email_content) # making problems
        else:
            print('No data - email not sent\n')
        clear_global()

pozoriste_job()

def check_Arena_Today():
    URL = 'https://starkarena.co.rs/lat/dogadjaji/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    try:
        page = requests.get(URL, headers=headers)
    except:
        send_email('ARENA DANAS', 'Error getting ARENA page!')
        return
    soup = BeautifulSoup(page.content, 'html.parser')

    head_info = soup.find('div', 'head_info')

    event_date = head_info.find('p', 'datetime').text.strip()[0:2]
    if(event_date.startswith('0')):
        event_date = event_date[1]

    event_name = head_info.find('h2').text.strip()

    event_description = head_info.find_all('p')[1].text.strip()

    if(int(event_date) == date.today().day and datetime.now().hour == 12 and datetime.now().minute == 0):
        send_email('ARENA DANAS', '{}\n{}'.format(event_name, event_description))

check_Arena_Today()
