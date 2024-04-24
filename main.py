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

# KUPLJENO !!!
# def check_dates_Voz():
#     append_to_global('Voz - Zvezdara Teatar:\n')
#     URL = 'https://zvezdarateatar.rs/predstava/voz/21/#'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
#     page = requests.get(URL, headers=headers)
#     soup = BeautifulSoup(page.content, 'html.parser')
#     dates = soup.find_all('span', 'predstava-dates')
    
#     if(dates):
#         for d in dates:
#             d = d.get_text().strip()
#             append_to_global(d + '\n')
#     else:
#         append_to_global('Error getting dates\n')
    
#     append_to_global('\n')

# KUPLJENO !!!
# def check_dates_Milutin():
#     append_to_global('Milutin - Zvezdara Teatar:\n')
#     URL = 'https://zvezdarateatar.rs/predstava/knjiga-o-milutinu-deo-prvi/10/'
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
#     try:
#         page = requests.get(URL, headers=headers)
#     except:
#         append_to_global('Error getting dates\n')
#         return
#     soup = BeautifulSoup(page.content, 'html.parser')
#     dates = soup.find_all('span', 'predstava-dates')
    
#     if(dates):
#         for d in dates:
#             d = d.get_text().strip()
#             append_to_global(d + '\n')
#     else:
#         append_to_global('Error getting dates\n')
    
#     append_to_global('\n')

def check_dates_Edip():
    append_to_global('Edip - JDP:\n')
    URL = 'https://www.jdp.rs/performance/edip/'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    try:
        page = requests.get(URL, headers=headers)
    except:
        append_to_global('Error getting dates\n')
        return
    soup = BeautifulSoup(page.content, 'html.parser')
    dates = soup.find_all('div', 'calendar__item-date js-date')
    content = ''
    for date_div in dates:
         day_div = date_div.find('div', 'day')
         day = day_div.find('strong').text
         month = day_div.find('span').text
         content += day+' '+month+'\n'

    if(dates):
        append_to_global(content)    
    else:
        append_to_global('Error getting dates\n')
    
    append_to_global('\n')

def check_dates_Edip_2():
    append_to_global('Edip - JDP v2:\n')
    URL = 'https://blagajna.jdp.rs/qrydata.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    form_data = {
        'q': '1',
        'godina': date.today().year,
        'mesec': date.today().month + 1,
        'sdsp': '1',
        'trazi': 'edip',
        'user_tipid': '',
        'sap': '1',
        'ss': '0',
        'tip_prikaza': '0',
    }
    try:
        results = requests.post(URL, headers=headers, data=form_data).json()
    except requests.RequestException as e:
        append_to_global('Error getting dates\n')
        
    if(len(results) > 0):
        for r in results:
            datum = r['datum']
            vreme = r['vreme'][0:5]
            datum_formatted = datetime.strptime(datum, '%Y-%m-%d').strftime('%d. %b')
            content = "{} - {}\n".format(datum_formatted, vreme)
            append_to_global(content)
            
    append_to_global('\n')
    
def check_dates_UrnebesnaTragedija():
    append_to_global('Urnebesna Tragedija - Narodno:\n')
    URL = 'https://www.narodnopozoriste.rs/lat/predstave/urnebesna-tragedija'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    try:
        page = requests.get(URL, headers=headers)
    except:
        append_to_global('Error getting dates\n')
        return
    soup = BeautifulSoup(page.content, 'html.parser')
    dates = soup.find_all('div', 'repertoarwide-entry-date')
    content = ''
    for date_div in dates:
        day = date_div.contents[1].strip()
        month = date_div.find('span', 'mesec').text
        content += day+' '+month+'\n'

    if(dates):
        append_to_global(content)
    else:
        append_to_global('Error getting dates\n')

    append_to_global('\n') 

def check_dates_Ljubavno_Pismo():
    append_to_global('Ljubavno Pismo - Atelje 212:\n')
    URL = 'https://bilet.atelje212.rs/qrydata.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    form_data = {
        'q': '1',
        'godina': date.today().year,
        'mesec': date.today().month + 1,
        'dan': '0',
        'sdsp': '1',
        'trazi': 'ljubavno',
        'user_tipid': '1',
        'sap': '1',
        'ss': '0',
        'tip_prikaza': '0',
    }
    '''
        TODO (IDEA):
        - switch to this query for every scraper
        - add listener that fetches every minute during the selected days of month
            - railway cron supports something like this:
                * 10-11 20,21,22,23,24,25 * * 
                (Every minute, between 10:00 and 11:59, on day 20, 21, 22, 23, 24, and 25 of the month)
        - only if results are found, send email
    '''
    try:
        results = requests.post(URL, headers=headers, data=form_data).json()
    except requests.RequestException as e:
        append_to_global('Error getting dates\n')
    
    if(len(results) > 0):
        for r in results:
            datum = r['datum']
            vreme = r['vreme'][0:5]
            datum_formatted = datetime.strptime(datum, '%Y-%m-%d').strftime('%d. %b')
            content = "{} - {}\n".format(datum_formatted, vreme)
            append_to_global(content)
            
    append_to_global('\n')

def pozoriste_job():
    if(date.today().day >= 20 and date.today().day < 26):
        # check_dates_Edip_2() TODO trying new stuff
        # check_dates_Voz() 
        # check_dates_Milutin()
        check_dates_Ljubavno_Pismo()
        check_dates_Edip()
        check_dates_UrnebesnaTragedija()
        # time.sleep(8) # in case scraping takes some time
        send_email('Pozoriste - datumi', global_email_content)
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

    if(int(event_date) == date.today().day):
        send_email('ARENA DANAS', '{}\n{}'.format(event_name, event_description))

check_Arena_Today()
