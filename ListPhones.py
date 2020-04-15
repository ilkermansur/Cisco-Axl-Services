from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
from zeep.exceptions import Fault
from zeep.plugins import HistoryPlugin
from requests import Session
from requests.auth import HTTPBasicAuth
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from lxml import etree
import getpass

# CUCM HostName/ IP Address
host = input("CUCM Hostname:")
# WSDL Service location download AXLToolKit from Call Manager
wsdl = input("WSDL Service path:")
# UserName and Password
user = input("Username: ")
pwd =  getpass.getpass()

location = 'https://{host}:8443/axl/'.format(host=host)
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"
session = Session()
session.verify = False
session.auth = HTTPBasicAuth(user, pwd)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
service = client.create_service(binding, location)

def listPhones(keyWord):
    try:
        reponse =  service.listPhone(searchCriteria={'name': keyWord},
                                    returnedTags={'name': '', 'model':'' ,'description':'' ,'ownerUserName':''})
        phones =  reponse['return'].phone
        print('Phone Name',',','Phone Model',',','Phone Description',',','Phone Owner')
        for phone in phones:
            print(phone.name,',', phone.model,',', phone.description, ',',phone.ownerUserName._value_1)
    except Exception as e:
        print(str(e))

# search keyword in CUCM, % can be used to cover the rest for example:
# CSF% => will locate all the devices that starts with the word CSF
# %CSF => will locate all the devices that ends with word CSF
# %CSF% => will locate all the devices that contains the word CSF
# in order to print all the devices in CUCM you can just use the keyword "%"
word = input("Enter Search KeyWord:")
listPhones(word)