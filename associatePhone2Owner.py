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

# in order to associate device to an owner we should pass a string list of all the devices and use updateUser service
# ==================================================================================================================
# Note => if we pass only the device that we want to associate it will override all the devices the user have if any.
# ===================================================================================================================
# to accomplish the association process we should get the user associated device to a list variable and then append the
# new device that we're planning to associate and finally associate the whole list to end user by using updateUser service


def associate(user, device):
    response =  service.getUser(userid=user)
    userProfile = response['return'].user
    try:
        phones = userProfile.associatedDevices.device
        phones.append(device)
    except:
        phones = [device]
    
    associated_devices = [{'device':phones}]
    response = service.updateUser(userid=user,
                                associatedDevices = associated_devices)
    print(response)

# inputs => device , User

username = input("Enter owner user id:")
device = input("Enter Device Name:")
associate(username, device)

        