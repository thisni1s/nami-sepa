import sys, os, time, datetime, csv
import pytoml as toml
from nami import Nami, TG_LEITER, TG_MITGLIED, TG_PASSIV

# load config
with open(os.path.expanduser('./pynami.conf'), 'r') as cfg:
    config = toml.load(cfg)

nami = Nami(config['nami'])
creditor = config['creditor']
payment_info = config['payment_info']


nami.auth()
print('Connected to Nami!')



def get_sepa_members():
    """
    gets all your members from the NaMi api, 
    important details like account information is missing here
    """
    search = {
        'mglStatusId': 'AKTIV',
        'mglTypeId': 'MITGLIED',
    }

    mgls = nami.search(search)

    print("Writing file...")
    with open(sys.argv[1], mode='w') as emails_file:
        emails_writer = csv.writer(emails_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        emails_writer.writerow(['ID', 'Vorname', 'Nachname', 'E-Mail'])
        for mgl in mgls:
            emails_writer.writerow([mgl['id'], mgl['vorname'], mgl['nachname'], mgl['email'] or mgl['emailVertretungsberechtigter']])

    



get_sepa_members()