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

# creating new device in call manager and configuring some of the device configurations
# Note: you can add / remove configurations from the function
# to check all the attribute names you can run python -mzeep wsdl 

def CreatePhone(deviceName, owner, line,description, devicePool, deviceType, phoneTemplateName, softkeyTemplateName, phoneProfile, mediaResourceListName, location,
callingSearchSpaceName, subscribeCallingSearchSpaceName, routePartition):
    try:
        resp = service.addPhone(phone={'name':deviceName,
        'description': description,
        'Product':deviceType,
        'class': 'Phone',
        'protocol': 'SIP',
        'protocolSide': 'User',
        'devicePoolName': devicePool ,
        'phoneTemplateName': phoneTemplateName,
        'softkeyTemplateName':softkeyTemplateName,
        'commonPhoneConfigName': phoneProfile,
        'callingSearchSpaceName': callingSearchSpaceName,
        'mediaResourceListName':mediaResourceListName,
        'locationName': location,
        'ownerUserName':{'_value_1': owner},
        'mobilityUserIdName':{'_value_1': owner},
        'rerouteCallingSearchSpaceName': callingSearchSpaceName,
        'subscribeCallingSearchSpaceName': subscribeCallingSearchSpaceName,
        'enableExtensionMobility':'true',
        'lines':{
            'line':{
                'index':1,
                'label':description,
                'display':description,
                'dirn':{
                    'pattern':line,
                    'routePartitionName': routePartition
                }
            }
        }
    })
        return resp
    except Exception as e:
        return str(e)

# Function Call => please modify the input params
CreatePhone('Phone1','Admin','+123456','NEW PHONE','phone_DP','Cisco 8845','TEST','TEST','TEST','TEST','Israel','TEST','TEST','GLOBE_DN')