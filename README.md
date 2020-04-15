# Cisco-Axl-Services
 
Cisco Call Manager's API - AXL Services using python
AXL Services will allow you to collect/ manage/ update/ add data to call manager through API.

Requirements :

1. install zeep - "pip install zeep"
2. download axlSQLToolKit from Call manager/ CUCM and add a reference to the file "axlsqltoolkit/schema/current/AXLAPI.wsdl"

Each script will prompt for the following params:

1. CUCM Hostname / IP Address
2. UserName for Cisco AXL
3. Password for Cisco AXL
4. WSDL location from the downloaded axlSQLToolKit. 
e.g 'file://C:/Users/7313482/Desktop/Projects/Tools/axlsqltoolkit/schema/current/AXLAPI.wsdl'
5. additional params based on the function your using such as deviceName, userid, etc.
