import date_checker

def check_dates():
    content = ''
    content += ('Milutin - Zvezdara Teatar:\n')
    URL = 'https://bilet.zvezdarateatar.rs/qrydata.php'
    content += date_checker.run(URL, 'МИЛУТИН')
    if(len(content) > len('Milutin - Zvezdara Teatar:\n')):
        return content
    else:
        return ''