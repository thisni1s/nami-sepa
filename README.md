# Nami-Sepa

Tool to create a Sepa-Xml file for all Members listed in the DPSG NAMI

## Usage

install the requirements with ``` pip3 install -r requirements.txt ```

copy the sample config ``` cp pynami.conf.sample pynami.conf ```

edit the config with the correct values

run programm ``` python3 namisepa.py name-of-output-file.xml```

sepa xml file will be in ``` out.xml ```

## NaMi

For this to work data needs to be inputted into NaMi in a specific way:

**Beware that the ```Kontonummer``` field is abused to store the signature date of the sepa mandate**

```

Zahlungsart:        Std Lastschrift         
Mitglieds-Nr:       111111                  # Prefilled member id
Kreditinstitut:     Sparkasse Köln          # Name of bank
Kontoinhaber:       Max Mustermann          # Account owner
Kontonummer:        31122023                # This is the signature date of the sepa mandate in format DDMMYYYY this is neccessary as there is no other way to input the signature date in NaMi
Bankleitzahl:                               # can be left empty
IBAN:               DE00000000000000000000  # IBAN
BIC/SWIFT:          SPKODE00XXX             # BIC      


```

## Credits

Special thanks to [@webratz](https://github.com/webratz) for creating the [pynami](https://github.com/webratz/pynami) Nami API implementation

And to [@raphaelm](https://github.com/raphaelm) for the [SEPA XML Generator](https://github.com/raphaelm/python-sepaxml)