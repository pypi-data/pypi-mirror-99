# Import packages
import os

class Headers:

    @classmethod
    def createHeaders(cls, json=False):
        credentials = eval((os.environ.get('aam_api_credentials')))
        request_headers = {"Authorization": "Bearer {0}".format(os.environ.get('aam_api_token')),
                          "x-api-key": credentials['client_id'],
                          "x-gw-ims-org-id": credentials['org_id']}
        if json:
            request_headers = {"accept": "application/json",
                               "content-type": "application/json",
                               "Authorization": "Bearer {0}".format(os.environ.get('aam_api_token')),
                               "x-api-key": credentials['client_id'],
                               "x-gw-ims-org-id": credentials['org_id']}
        
        return request_headers