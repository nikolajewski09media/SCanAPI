import csv

def switch_Emails(argument):
    emails = {
        'Erduan': 'bytyqi@09media.de',
        'Rami': 'rami@09media.de',
        'Rafea': 'rafea@09media.de',
        'Paul': 'jungkind@09media.de',
        'Mané': 'hovhanisyan@09media.de'
        #Zum testen
        # 'Erduan': 'nikolajewski@09media.de',
        # 'Rami': 'nikolajewski@09media.de',
        # 'Rafea': 'nikolajewski@09media.de',
        # 'Paul': 'nikolajewski@09media.de',
        # 'Mané': 'nikolajewski@09media.de',
    }
    return emails.get(argument, 'Invalid Webdesinger')

def compare2csv(domain):
    zuteilung = {}
    with open('zuteilungwebseiten.csv', 'r') as read_obj:
        csv_reader = csv.DictReader(read_obj, delimiter=';')
        for row in csv_reader:
            zuteilung.update({row['domain']: row['webdesigner']})
        email = switch_Emails(zuteilung[domain.lower()])
        webdesigner = zuteilung[domain.lower()]
    return email, webdesigner





