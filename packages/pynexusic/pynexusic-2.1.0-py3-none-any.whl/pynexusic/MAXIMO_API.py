import requests
import base64
import datetime
import traceback
import json

############################# Maximo REST API Class ############################
class MAXIMO_REST():
    """
        Maximo API class allows the user to communicate with Maximo REST API using python

        Prerequisites:
        -------------
            - Python > 3.7
            - Maximo access
    """


    _error_msgs = ['An existing connection was forcibly closed by the remote host',
                   'Remote end closed connection without response']

    def __init__(self, base_url, username=None, password=None, api_key=None,
                 authentication_type='LDAP BASIC',
                 max_attempts=1, timeout=None,
                 verbose=False, verify=True):
        """
            The constructor for MAXIMO_REST class.

            Parameters:
            ----------
                maximo_url (string): Maximo URL
                username (string - optional): Default value None.
                password (string - optional): Default value None.
                api_key (string - optional): Default value None.
                authentication_type (string - optional): The only value supported LDAP BASIC (default value LDAP BASIC)
                max_attempts (int - optional): Maximum number of attempts if disconnected (default value 1)
                timeout (int - optional): Timeout threshold in seconds (default value None)
                verbose (bool - optional): Print internal messages if True (default value False)
                verify (bool - optional): By pass SSL verification if True (default value True)

            Returns:
            -------
                None
        """

        assert authentication_type in ['LDAP BASIC'], 'Incorrect authentication type'

        if username == None:
            raise Exception('Username is empty, please provide a valid username')

        if password == None:
            raise Exception('Password is empty, please provide a valid password')

        self.base_url = base_url
        self.authentication_type = authentication_type
        self.username = username
        self.password = password
        self.api_key = api_key
        self.max_attempts = max_attempts   # TODO: Functionality to be added
        self.timeout = timeout   # TODO: To be added to the REST calls
        self.verbose = verbose
        self.verify = verify
        self.api_key = self.generate_base64(self.username + ':' + self.password)
        self.session = None
        self.authenticate()

    ######################################################################################
    def generate_base64(self, value):
        return str(base64.b64encode(bytes(value, 'utf-8')), "utf-8")

    ######################################################################################
    def validate_and_return_response(self, response, message, raw=False):
        if response.status_code in [200, 201, 204]:
            if raw:
                return response.raw, response.status_code
            else:
                return response.json(), response.status_code
        else:
            return str(message) + str(response.status_code) + ': ' + str(response.text), \
                   response.status_code

    ######################################################################################
    def authenticate(self, verbose=False):
        if self.verbose or verbose:
            print('Authenticating with Maximo...')

        if self.authentication_type == 'LDAP BASIC':
            url = self.base_url + '/maximo/j_security_check?j_username=' + \
                  self.username + '&j_password=' + self.password

            self.session = requests.Session()
            self.session.get(url)
        else:
            raise Exception(self.authentication_type + ' authentication type not supported')

    ######################################################################################
    def mxapi_get_request(self, url):
        if self.authentication_type == 'LDAP BASIC':
            return self.session.get(url,
                                    headers={'Authorization': 'Basic' + self.api_key},
                                    verify=self.verify)
        else:
            raise Exception(self.authentication_type + ' authentication type not supported')

    ######################################################################################
    def get_table(self, tableName, pageSize=None, current_attempt=1,
                 verbose=False, select=None, where=None, orderBy=None,
                 pageNum=1, stablePaging=False):
        if self.verbose or verbose:
            print('Getting ' + str(tableName) + '...')

        # Adding /oslc/ part to the baseURI
        url = self.base_url + '/maximo/oslc/os/' + tableName

        # Check page size
        if pageSize != None:
            if '?' in url:
                url += '&oslc.pageSize=' + str(pageSize)
            else:
                url += '?oslc.pageSize=' + str(pageSize)

        # Add select query
        if select != None:
            if '?' in url:
                url += '&oslc.select=' + str(select)
            else:
                url += '?oslc.select=' + str(select)

        # Add where query
        if where != None:
            if '?' in url:
                url += '&oslc.where=' + str(where)
            else:
                url += '?oslc.where=' + str(where)

        # Add order by query
        if orderBy != None:
            if '?' in url:
                url += '&oslc.orderBy=+' + str(orderBy)
            else:
                url += '?oslc.orderBy=+' + str(orderBy)

        # Check stable paging
        if stablePaging:
            if '?' in url:
                url += '&stablepaging=true'
            else:
                url += '?stablepaging=true'

        # Check pageNum
        if pageNum > 1:
            if '?' in url:
                url += '&pageno=' + str(pageNum)
            else:
                url += '?pageno=' + str(pageNum)

        # Execute request
        has_more_records = True
        result = {'members': []}
        try:
            while has_more_records:
                response = self.mxapi_get_request(url)
                resp_result, resp_code = self.validate_and_return_response(response,
                                                                           'Get ' + tableName + ' table error')
                result['members'].extend(resp_result['rdfs:member'])

                if 'oslc:nextPage' in resp_result['oslc:responseInfo']:
                    prev_pageNum = pageNum
                    pageNum += 1
                    if '&pageno=' in url:
                        url = url.replace('&pageno=' + str(prev_pageNum), '&pageno=' + str(pageNum))
                    else:
                        url += '&pageno=' + str(pageNum)
                else:
                    has_more_records = False

            return result, resp_code
        except Exception as e:
            for error_msg in MAXIMO_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if current_attempt <= self.max_attempts:
                        self.authenticate()
                        return self.get_table(tableName, pageSize=pageSize,
                                              current_attempt=current_attempt,
                                              verbose=verbose, select=select,
                                              where=where, orderBy=orderBy,
                                              pageNum=pageNum,
                                              stablePaging=stablePaging)

            errorMsg = traceback.format_exc()
            raise Exception('Error getting data from table: ' + str(tableName) + '\n' + errorMsg)

######################################################################################
################################### Start Script #####################################
if __name__ == '__main__':
    maximoURL = ''
    username = ''
    password = ''

    mx_obj = MAXIMO_REST(maximoURL, username, password)
    print(mx_obj.getTable('mxasset', select='*'))