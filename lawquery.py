# Runs a KQL query against log analytics workspace and yields the results as a JSON object.
import requests
import json
import os
import datetime
from math import floor

test = '''{
  "tables": [
    {
      "name": "PrimaryResult",
      "columns": [
        {
          "name": "TenantId",
          "type": "string"
        },
        {
          "name": "Computer",
          "type": "string"
        },
        {
          "name": "TimeGenerated",
          "type": "datetime"
        },
        {
          "name": "SourceSystem",
          "type": "string"
        },
        {
          "name": "StartTime",
          "type": "datetime"
        },
        {
          "name": "EndTime",
          "type": "datetime"
        },
        {
          "name": "ResourceUri",
          "type": "string"
        },
        {
          "name": "LinkedResourceUri",
          "type": "string"
        },
        {
          "name": "DataType",
          "type": "string"
        },
        {
          "name": "Solution",
          "type": "string"
        },
        {
          "name": "BatchesWithinSla",
          "type": "long"
        },
        {
          "name": "BatchesOutsideSla",
          "type": "long"
        },
        {
          "name": "BatchesCapped",
          "type": "long"
        },
        {
          "name": "TotalBatches",
          "type": "long"
        },
        {
          "name": "AvgLatencyInSeconds",
          "type": "real"
        },
        {
          "name": "Quantity",
          "type": "real"
        },
        {
          "name": "QuantityUnit",
          "type": "string"
        },
        {
          "name": "IsBillable",
          "type": "bool"
        },
        {
          "name": "MeterId",
          "type": "string"
        },
        {
          "name": "LinkedMeterId",
          "type": "string"
        },
        {
          "name": "Type",
          "type": "string"
        }
      ],
      "rows": [
        [
          "b438b4f6-912a-46d5-9cb1-b44069212abc",
          "ContosoSQLSrv1",
          "2017-08-24T06:59:59.0000000Z",
          "OMS",
          "2017-08-24T06:00:00.0000000Z",
          "2017-08-24T06:59:59.0000000Z",
          "/subscriptions/e4272367-5645-4c4e-9c67-3b74b59a6982/resourcegroups/contosoazurehq/providers/microsoft.operationalinsights/workspaces/contosoretail-it",
          null,
          "Perf",
          "LogManagement",
          "1",
          "0",
          "0",
          "1",
          "1.286",
          "0.076408",
          "MBytes",
          "true",
          "a4e29a95-5b4c-408b-80e3-113f9410566e",
          "00000000-0000-0000-0000-000000000000",
          "Usage"
        ],
        [
          "b438b4f6-912a-46d5-9cb1-b44069212abc",
          "Store010Web3",
          "2017-08-24T06:59:59.0000000Z",
          "OMS",
          "2017-08-24T06:00:00.0000000Z",
          "2017-08-24T06:59:59.0000000Z",
          "/subscriptions/e4272367-5645-4c4e-9c67-3b74b59a6982/resourcegroups/contosoazurehq/providers/microsoft.operationalinsights/workspaces/contosoretail-it",
          null,
          "Perf",
          "LogManagement",
          "1",
          "0",
          "0",
          "1",
          "1.7",
          "0.106767",
          "MBytes",
          "true",
          "a4e29a95-5b4c-408b-80e3-113f9410566e",
          "00000000-0000-0000-0000-000000000000",
          "Usage"
        ]
      ]
    }
  ]
}'''

class LawTable():
    def __init__(self, table:dict):
        self.fields = table['tables'][0]['columns']
        self.rows = table['tables'][0]['rows']

    def yield_events(self):
        for row in self.rows:
            event = {}
            for i in range(len(self.fields)):
                name = self.fields[i]['name']
                val_type = self.fields[i]['type']
                event[name] = self.make_type(val_type, row[i])
                if name == "TimeGenerated":
                    print(row[i])
                    _time = floor(datetime.datetime.strptime(row[i][:26], "%Y-%m-%dT%H:%M:%S.%f").timestamp())
                    print(_time)
            event['_raw'] = json.dumps(event, indent=2)
            # This is out here because I don't want _time to appear in _raw
            if _time:
              event['_time'] = _time
            yield event

    def make_type(self, type:str, val:str):
        if type == "long":
            return int(val)
        if type == "real":
            return float(val)
        if type == "bool":
            return bool(val)
        if type == "dynamic":
            return json.loads(val)
        else:
            return val
      

class LawWorkspace():
    def __init__(self, tenant_id, client_id, client_secret, workspace_id):
        self.workspace_id = workspace_id
        self.access_token = self.get_access_token(tenant_id, client_id, client_secret)

    def get_access_token(self, tenant_id, client_id, client_secret) -> str:
        """
        Gets an Azure Graph API bearer token and returns the result
        """
        # Construct the URL for the Azure AD token endpoint
        url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        
        # Set up the headers with content type
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        # Prepare the payload with the client ID, secret, and scope
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://api.loganalytics.io/.default",
            "grant_type": "client_credentials"
        }
        
        # Make the POST request to get the access token
        response = requests.post(url, headers=headers, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            print("Access token successful")
            return response.json()["access_token"]
        else:
            raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

    def run_kql_query(self, query) -> LawTable:
        # Construct the URL for the Log Analytics API endpoint
        url = f"https://api.loganalytics.io/v1/workspaces/{self.workspace_id}/query"
        
        # Set up the headers with authorization and content type
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # Prepare the payload with the KQL query
        payload = json.dumps({
            "query": query
        })
        
        # Make the POST request to run the query
        response = requests.post(url, headers=headers, data=payload)
        
        # Check if the request was successful
        if response.status_code == 200:
            return LawTable(response.json())
        else:
            raise Exception(f"Failed to run KQL query: {response.status_code} - {response.text}")


if __name__ == '__main__':
    tenant = os.environ.get('tenant_id')
    workspace = os.environ.get('workspace_id')
    client = os.environ.get('client_id')
    secret = os.environ.get('client_secret')
    law = LawWorkspace(tenant, client, secret, workspace)

    results = law.run_kql_query("""MicrosoftGraphActivityLogs | extend test=dynamic('[{"test": "something"}, {"anothertest": [1, 2, 3]}]')""")
    for event in results.yield_events():
        print(json.dumps(event, indent=2))

    # test = LawTable(json.loads(test))
    # for event in test.yield_events():
    #     print(json.dumps(event, indent=2))