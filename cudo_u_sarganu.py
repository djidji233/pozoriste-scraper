import date_checker

def check_dates():
    content = ''
    content += ('Cudo u Sarganu:\n')
    URL = 'https://blagajna.jdp.rs/qrydata.php'
    content += date_checker.run(URL, 'CUDO U SARGANU')
    if(len(content) > len('Cudo u Sarganu:\n')):
        return content
    else:
        return ''