import os, time, datetime
import pytoml as toml
from nami import Nami, UG_JUPFI, UG_PFADI, UG_ROVER
from schemas import SepaMember, SepaMandate
from sepaxml import SepaDD
from schwifty import BIC, IBAN

# load config
with open(os.path.expanduser('./pynami.conf'), 'r') as cfg:
    config = toml.load(cfg)

nami = Nami(config['nami'])
creditor = config['creditor']
payment_info = config['payment_info']


nami.auth()
print('Connected to Nami!')


payment_config = {
    "name": creditor['name'],
    "IBAN": creditor['iban'],
    "BIC": creditor['bic'],
    "batch": True,
    "creditor_id": creditor['creditor_id'],  # supplied by your bank or financial authority
    "currency": "EUR",  # ISO 4217
}
sepa = SepaDD(payment_config, schema="pain.008.001.02", clean=True)

def get_sepa_members():
    """
    gets all your members from the NaMi api, 
    important details like account information is missing here
    """
    search = {
        'mglStatusId': 'AKTIV',
        'mglTypeId': 'MITGLIED',
    #    'nachname': 'Sieferlinger',
    #    'untergliederungId': UG_ROVER
    }

    mgls = nami.search(search)
    mitglieder = []

    for mgl in mgls:
        mitglied = nami.get_mitglied_obj(mgl['id_id'])
        mitglied_mandate = SepaMandate(mitglied['kontoverbindung']['kontoinhaber'], mitglied['kontoverbindung']['institut'], mitglied['kontoverbindung']['iban'], mitglied['kontoverbindung']['bic'], mitglied['kontoverbindung']['kontonummer'])
        email = mitglied['email'] or mitglied['emailVertretungsberechtigter']
        sepa_mitglied = SepaMember(mitglied['id'], mitglied['mitgliedsNummer'], mitglied['vorname'].split()[0], mitglied['nachname'], email, mitglied['beitragsart'], mitglied_mandate)
        mitglieder.append(sepa_mitglied)
        print(f"Got: {sepa_mitglied.firstName} {sepa_mitglied.lastName}")
        time.sleep(0.15) # try not to overwhelm NaMi

    print(f"Got {len(mitglieder)} Members")
    return mitglieder

def check_payment(payment) -> bool:
    for key, val in payment.items():        
        if not val:
            print(f"Wrong {key} in {payment}")
            return False
    return True

def get_payment_amount(feeType: str) -> int:
    if(feeType == "Voller Beitrag"):
        return int(payment_info['fee_normal'] * 100)
    elif(feeType == "Familienermäßigt"):
        return int(payment_info['fee_family'] * 100)
    elif(feeType == "Sozialermäßigt"):
        return int(payment_info['fee_social'] * 100)
    else:
        return int(payment_info['fee_normal'] * 100)




sepa_member_list = get_sepa_members()

col_date_arr = payment_info['collection_date'].split()
collection_date = datetime.date(int(col_date_arr[0]), int(col_date_arr[1]), int(col_date_arr[2]))

for entry in sepa_member_list:
    if entry.sepaMandate.date != "" and entry.sepaMandate.iban != "":
        date_str = entry.sepaMandate.date
        date = datetime.date(int(date_str[4:]), int(date_str[2:4]), int(date_str[:2]))
        bic = entry.sepaMandate.bic or IBAN(entry.sepaMandate.iban).bic.formatted.replace(' ', '') # calculate missing bics


        payment = {
            "name": entry.sepaMandate.owner,
            "IBAN": entry.sepaMandate.iban,
            "BIC": bic,
            "amount": get_payment_amount(entry.feeType),  # in cents
            "type": "RCUR",  # FRST,RCUR,OOFF,FNAL
            "collection_date": collection_date,
            "mandate_id": f"{entry.memberId}-{entry.firstName}-{entry.lastName}",
            "mandate_date": date,
            "description": f"{creditor['description_text']} {entry.firstName} {entry.lastName}"
        }
        if check_payment(payment):
            sepa.add_payment(payment)

print("Writing file...")
with open("out.xml", "wb") as f:
    f.write(sepa.export(validate=True)) 