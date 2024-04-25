import date_checker

def check_dates():
    content = ''
    content += ('Ljubavno Pismo - Atelje 212:\n')
    URL = 'https://bilet.atelje212.rs/qrydata.php'
    content += date_checker.run(URL, 'LJUBAVNO')
    if(len(content) > len('Ljubavno Pismo - Atelje 212:\n')):
        return content
    else:
        return ''