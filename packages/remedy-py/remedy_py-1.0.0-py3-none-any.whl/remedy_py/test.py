from RemedyAPIClient import RemedyClient
import os

# works

# host = os.environ['REMEDY_HOST'] or 
# user = os.environ['REMEDY_USER']
# password = os.environ['REMEDY_PASSWORD']
host="35.153.129.209"
user="appadmin"
password="password"
port = 8008

ENTRY_TEMPLATE = {
    "First_Name": "Allen",
    "Last_Name": "Allbrook",
    "Description": "REST API: Incident Creation",
    "Impact": "1-Extensive/Widespread",
    "Urgency": "1-Critical",
    "Status": "Assigned",
    "Reported Source": "Direct Input",
    "Service_Type": "User Service Restoration",
    "z1D_Action": "CREATE"
}  

CLOSE_TEMPLATE = {                                               
    "Description" : "Rest API: Resolve Incident using RestAPI",                                               
    "Status" : "Resolved",                                               
    "Status_Reason" : "Future Enhancement",                                               
    "Resolution" : "Test Resolution Text"
}


FORM_NAME = "HPD:IncidentInterface_Create"
RETURN_VALUES = ["Incident Number", "Request ID"]

try:
    client = RemedyClient(host, user, password, port=port, verify=False)

    # create an incident, save identifying data
    incident, _ = client.create_form_entry(FORM_NAME, ENTRY_TEMPLATE, RETURN_VALUES)
    incident_id = incident["values"]["Incident Number"]
    request_id = incident["values"]["Request ID"]

    # retrive incident data based on ID above
    incident, _ = client.get_form_entry(FORM_NAME, request_id)

    # make an update to an incident
    incident, _ = client.update_form_entry(FORM_NAME, request_id, CLOSE_TEMPLATE)

    # delete the incident
    incident, _ = client.delete_form_entry(FORM_NAME, request_id)

    #logout
    client.release_token()

    print("let's go!!")

except Exception as e:
    print(e)
    