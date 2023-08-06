import requests
from compredict.exceptions import ClientError, ServerError
from tempfile import NamedTemporaryFile

from compredict.exceptions import Error


class Connection:

    def __init__(self, url, token=None):
        """
        Class response for HTTP requests and communication.

        :param url: The base url string
        :param token: The API authorization token.
        """
        self.url = url
        self.last_error = False
        self.fail_on_error = False
        self.ssl = False
        self.response = None
        self.headers = dict(Accept='application/json')
        self.last_request = None
        if token is not None:
            self.headers['Authorization'] = 'Token ' + token

    def set_token(self, token):
        """
        Set the token for authorization.

        :param token: String API Key
        :return: None
        """
        self.headers['Authorization'] = 'Token ' + token

    def POST(self, endpoint, data, files=None):
        """
        Responsible for sending POST request and uploading files if specified.

        :param endpoint: the endpoint of the URL.
        :param data: The form data to be sent.
        :param files: The files to be sent.
        :return: JSON if request is correct otherwise false.
        """
        address = self.url + endpoint
        if files is not None:
            if 'Content-Type' in self.headers:
                del self.headers['Content-Type']
        else:
            self.headers['Content-Type'] = 'application/json'
        self.last_request = requests.post(address, files=files, data=data, headers=self.headers)
        return self.__handle_response(self.last_request)

    def GET(self, endpoint):
        """
        Responsible for sending GET requests.

        :param endpoint: the targeted endpoint.
        :return: JSON if request is correct otherwise false.
        """
        address = self.url + endpoint
        self.headers['Content-Type'] = 'application/json'
        self.last_request = requests.get(address, None, headers=self.headers)
        return self.__handle_response(self.last_request)

    def __handle_response(self, request):
        """
        Handles the requests based on the status code. In addition it raises exception if fail_on_error is True.

        :param request: the request made to the URL.
        :return: JSON if request is correct otherwise false.
        """
        if 400 <= request.status_code <= 499:
            if self.fail_on_error:
                raise ClientError(request.json())
            else:
                error = Error(request.json(), request.status_code)
                self.last_error = error
                return False

        elif 500 <= request.status_code <= 599:
            if self.fail_on_error:
                raise ServerError(request.json())
            else:
                error = Error(request.json(), request.status_code)
                self.last_error = error
                return False

        if '/template' in request.url or '/graph' in request.url:
            ext = '.png' if request.headers['Content-Type'] == 'image/png' else '.json'
            response = NamedTemporaryFile(suffix=ext)
            response.write(request.content)
            response.seek(0)
        else:
            response = request.json()

        return response
