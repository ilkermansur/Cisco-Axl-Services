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

# function will update some device configurations: phone name, phone description , device pool and owner user id
# phone name is provided to locate the device and the rest is to update the device configurations
# note: this function wont associate the device to the owner , it will add the owner to the device 

def updatePhone(phoneName, newPhoneName ,phoneDescription, devicePool, Owner):
    try:
        response =  service.updatePhone(
            name=phoneName,
            newName=newPhoneName,
            description=phoneDescription,
            devicePoolName=devicePool,
            ownerUserName=Owner
        )
        print(response)
    except Exception as e:
        print(str(e))

# configurations input
phone =  input("Enter Phone Name:")
newName = input("Enter Phone New Name:")
description = input("Enter Phone Description:")
pool = input("Enter Device Pool Name:")
userid = input("Enter Owner User ID:")
updatePhone(phone,newName,description,pool,userid)
