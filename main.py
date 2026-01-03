import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
from datetime import datetime, date
from dotenv import load_dotenv
import os
import logging
import sys
import json
import urllib3
import cudo_u_sarganu

# Disable SSL warnings for sites with certificate issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def check_pozoriste():
    logging.info('| Running Pozoriste job')
    # append_to_global(urnebesna_tragedija.check_dates()) # left as example
    append_to_global(cudo_u_sarganu.check_dates())
    
    if(len(global_email_content) > 0):
        logging.info('-> Pozoriste email sending...')
        send_email('Pozoriste - datumi', global_email_content)
        logging.info('-> Pozoriste email sent!')
    else:
        logging.info('-> Pozoriste email not sent (no dates)')
    clear_global()

def check_arena():
    logging.info('| Running Arena job')
    URL = 'https://arenabeograd.com/listadogadjaja/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    try:
        page = requests.get(URL, headers=headers, verify=False)
    except Exception as e:
        logging.error('!!! Exception: ' + str(e))
        send_email('Arena - Error', 'Error getting Arena page')
        return
    soup = BeautifulSoup(page.content, 'html.parser')

    head_info = soup.find("div", class_='portfolio-classic-content')

    event_date = 99 # TODO: map dates correctly

    # if(event_date.startswith('0')):
    #     event_date = event_date[1]

    event_name = head_info.h3.text.strip()

    event_description = head_info.find_all('span')[1].text.strip()

    if(int(event_date) == date.today().day and datetime.now().hour == 12):
        logging.info('-> Arena email sending...')
        send_email('Arena danas!', '{}\n{}'.format(event_name, event_description))
        logging.info('-> Arena email sent!')
    else:
        logging.info('-> Arena email not sent (no event today)')

def check_sava_centar():
    logging.info('| Running Sava Centar job')
    URL = 'https://savacentar.rs/dogadjaji-u-sava-centru/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    
    try:
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # Find the script tag containing our data
        script = soup.find('script', {'id': 'codemine-calendar-js-js-extra'})
        if not script:
            raise Exception('Script tag not found')
            
        # Extract the JSON data
        data_text = script.text
        json_start = data_text.find('CMCAL_vars_8 = ') + len('CMCAL_vars_8 = ')
        json_end = data_text.find('};', json_start) + 1
        json_str = data_text[json_start:json_end]
        # Parse JSON and get events
        calendar_data = json.loads(json_str)
        events = calendar_data.get('all_events', [])

        # Find today's events
        today = date.today()
        todays_events = [
            event for event in events 
            if event['start'].split('T')[0] == today.strftime('%Y-%m-%d')
        ]
        
        if todays_events and datetime.now().hour == 12:
            logging.info('-> Sava Centar email sending...')
            email_content = '\n\n'.join([
                f"{event['title']}\n"
                f"Vreme: {event.get('vreme_dogadjaja', 'Unknown')}\n"
                for event in todays_events
            ])
            send_email('Sava Centar danas!', email_content)
            logging.info('-> Sava Centar email sent!')
        else:
            logging.info('-> Sava Centar email not sent (no events today)')
            
    except Exception as e:
        logging.error(f'!!! Exception: {e}')
        send_email('Sava Centar danas!', 'Error getting Sava Centar page')
        
# RUN
# check_pozoriste()
# check_arena()
# check_sava_centar()