# Nami-Sepa

Tool to create a Sepa-Xml file for all Members listed in the DPSG NAMI

## Usage

install the requirements with ``` pip3 install -r requirements.txt ```

copy the sample config ``` cp pynami.conf.sample pynami.conf ```

edit the config with the correct values

run programm ``` python3 namisepa.py ```

sepa xml file will be in ``` out.xml ```

## Credits

Special thanks to [@webratz](https://github.com/webratz) for creating the [pynami](https://github.com/webratz/pynami) Nami API implementation

And to [@raphaelm](https://github.com/raphaelm) for the [SEPA XML Generator](https://github.com/raphaelm/python-sepaxml)