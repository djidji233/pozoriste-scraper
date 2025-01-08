import date_checker

def check_dates():
    content = ''
    content += ('Voz - Zvezdara Teatar:\n')
    URL = 'https://bilet.zvezdarateatar.rs/qrydata.php'
    content += date_checker.run(URL, 'VOZ')
    if(len(content) > len('Voz - Zvezdara Teatar:\n')):
        return content
    else:
        return ''