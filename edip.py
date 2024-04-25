import date_checker

def check_dates():
    content = ''
    content += ('Edip - JDP:\n')
    URL = 'https://blagajna.jdp.rs/qrydata.php'
    content += date_checker.run(URL, 'EDIP')
    if(len(content) > len('Edip - JDP:\n')):
        return content
    else:
        return ''