import requests
import json
from requests.auth import HTTPBasicAuth
#from requests_kerberos import HTTPKerberosAuth
from requests_ntlm import HttpNtlmAuth

############################# OSI PI Web API Class ############################
class OSIPI_WebAPI():
    """
    OSI PI Web API class allows the user to communicate with OSI PI web API using python

    Prerequisites:
    -------------
        - Python > 3.7
        - OSI PI access

    OSI PI Documentation:
    --------------------
        The OSI PI Web API documentation can be found in the bellow link:
        https://techsupport.osisoft.com/Documentation/PI-Web-API/help.html
    """

    def __init__(self, piwebapi_url, username, password, authentication_type='basic',
                 max_attempts=1, timeout=None,
                 verbose=False, verify=True):
        """
            The constructor for OSIPI_WebAPI class.

            Parameters:
            ----------
                piwebapi_url (string): OSI PI base URL.
                username (string): OSI PI username.
                password (string): OSI PI password.
                authentication_type (string - optional): This can be either ntlm or basic (default value basic).
                max_attempts (int - optional): Maximum number of attempts if disconnected (default value 1).
                timeout (int - optional): Timeout threshold in seconds (default value None).
                verbose (bool - optional): Print internal messages if True (default value False).
                verify (bool - optional): By pass SSL verification if True (default value True).

            Returns:
            -------
                None
        """
        assert authentication_type.lower() in ['ntlm', 'basic'], 'Incorrect security method'
        self.piwebapi_url = piwebapi_url
        self.authentication_type = authentication_type
        self.username = username
        self.password = password
        self.max_attempts = max_attempts   # TODO: Functionality to be added
        self.timeout = timeout  # TODO: To be added to the REST calls
        self.verbose = verbose
        self.verify = verify

        self.authentication_type = self.authenticate(self.authentication_type, self.username, self.password)
        self.sys_links = self.get_system_links()

    ########################################################################################################
    def authenticate(self, authentication_type, username, password):
        """
            Authenticate and create API call security method

            Parameters:
            ----------
                authentication_type string:  authentication method to use:  basic or ntlm.
                username string: The user's credentials name.
                password string: The user's credentials password.

            Returns:
            -------
                TBD
        """

        if authentication_type.lower() == 'basic':
            security_auth = HTTPBasicAuth(username, password)
        elif authentication_type.lower() == 'ntlm':
            security_auth = HttpNtlmAuth(username, password)
        #else:
        #    security_auth = HTTPKerberosAuth(mutual_authentication='REQUIRED',
        #                                     sanitize_mutual_error_response=False)

        return security_auth

    ######################################################################################
    def validate_and_return_response(self, response, message='', raw=False):
        if response.status_code in [200]:
            if raw:
                return response.raw, response.status_code
            else:
                return response.json(), response.status_code
        else:
            return str(message) + str(response.status_code) + ': ' + str(response.text), \
                   response.status_code

    ########################################################################################################
    def webapi_get_request(self, url, pageSize=None, message='', raw=False):
        if pageSize != None:
            url = url + '/?maxCount=' + str(pageSize)

        response = requests.get(url, auth=self.authentication_type, verify=self.verify)

        resp, resp_status = self.validate_and_return_response(response, message=message, raw=raw)

        return resp, resp_status

    ########################################################################################################
    def get_system_links(self, pageSize=None):
        result = {}
        links, links_status = self.webapi_get_request(self.piwebapi_url, pageSize=pageSize)
        for link in links['Links']:
            if link in ['DataServers', 'AssetServers']:
                response, resp_status = self.webapi_get_request(links['Links'][link], pageSize=pageSize)
                result[link] = {'Link': links['Links'][link], 'WebID': response['Items'][0]['WebId']}
        return result

    ########################################################################################################
    def getPointsList(self, pageSize=None):
        points_url = self.sys_links['DataServers']['Link'] + r'/' + self.sys_links['DataServers']['WebID'] + r'/points'
        points_resp, points_resp_status = self.webapi_get_request(points_url, pageSize=pageSize)
        return points_resp['Items'], points_resp_status

    ########################################################################################################
    def getStreamData(self, webID, searchType='end', parameters=None, pageSize=None):
        assert searchType.lower() in ['end', 'interpolated', 'recorded',
                                      'plot', 'summary', 'value'], searchType + ' search type not supported'

        if parameters == None:
            url = self.piwebapi_url + r'/streams/' + str(webID) + r'/' + searchType.lower()
        else:
            url = self.piwebapi_url + r'/streams/' + str(webID) + r'/' + searchType.lower() + '?' + parameters

        resp, resp_status = self.webapi_get_request(url, pageSize=pageSize)
        return resp, resp_status

    ########################################################################################################
    def getStreamDataSummary(self, webID, startTime=None, endTime=None, summaryType=None, pageSize=None):
        assert summaryType in ['Total', 'Average', 'Minimum', 'Maximum', 'Range',
                               'StdDev', 'PopulationStdDev', 'Count', 'PercentGood',
                               'TotalWithUOM', 'All', 'AllForNonNumeric'], summaryType + ' summary type not supported'
        parameters = None
        if startTime != None:
            parameters = 'startTime=' + str(startTime)

        if endTime != None:
            if parameters == None:
                parameters = 'endTime=' + str(endTime)
            else:
                parameters += '&endTime=' + str(endTime)

        if summaryType != None:
            if parameters == None:
                parameters = 'summaryType=' + str(summaryType)
            else:
                parameters += '&summaryType=' + str(summaryType)

        resp, resp_status = self.getStreamData(webID, searchType='summary', parameters=parameters, pageSize=pageSize)
        return resp, resp_status

    ########################################################################################################
    def getPointAttributes(self, webID, pageSize=None):
        url = self.piwebapi_url + r'/points/' + str(webID) + r'/attributes'
        resp, resp_status = self.webapi_get_request(url, pageSize=pageSize)
        return resp, resp_status

############################################################################################################
############################################################################################################
if __name__ == '__main__':
    pass