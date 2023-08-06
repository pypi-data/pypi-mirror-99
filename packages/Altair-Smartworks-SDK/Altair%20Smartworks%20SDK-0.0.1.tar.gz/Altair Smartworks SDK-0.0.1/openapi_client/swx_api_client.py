"""Module to fetch auth token from SWX Auth Server and update headers for requests"""

from openapi_client.api_client import ApiClient
from json import loads


class SwxApiClientException(Exception):
    """An exception originating from SwxApiClient"""


class SwxApiClient(ApiClient):
    """Subclass of APIClient that allows basic auth"""

    def __init__(self, *args, **kwargs):
        try:
            super(SwxApiClient, self).__init__(configuration=kwargs.get('configuration', None))

            self.client_id = kwargs.get('client_id', None)
            self.client_secret = kwargs.get('client_secret', None)
            self.scope = kwargs.get('scope', None)
            if None in [self.client_id, self.client_secret, self.scope]:
                raise Exception(
                    'Cannot initialize SwxApiClient with [client_id, client_secret, scope]=%s' %
                    [self.client_id, self.client_secret, self.scope]
                )

            self.request_url = self.configuration.host + '/oauth2/token'
            self.headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            self.auth_params = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': self.scope
            }

            # Do auth implicitly
            if not kwargs.get('defer_auth', False):
                self.do_auth()

        except Exception as error:
            raise SwxApiClientException(
                'While initializing SwxApiClient: {}'.format(error)
            )

    def do_auth(self):
        """Populate default headers with access token from Auth API"""
        try:
            try:
                token_response = self.request(
                    'POST',
                    self.request_url,
                    headers=self.headers,
                    post_params=self.auth_params
                )
            except AttributeError as error:
                raise Exception('While making request {}, {}'.format(
                    self.request_url, error))

            # For an invalid request, Auth API still returns "200" response with
            # error status code in response body
            response_data = loads(token_response.data)
            response_error_code = None
            if 'error_auth_backend' in response_data:
                response_error_code = response_data['error_auth_backend'].get(
                    'http_status_code',
                    None
                )
            if token_response.status != 200 or response_error_code is not None:
                raise Exception('While making request {}; status {},\
                    error_status {} returned with error message {}'.format(
                        self.request_url,
                        token_response.status,
                        response_error_code,
                        response_data['error_auth_backend'].get('http_body', None)
                        ))

            access_token = response_data.get('access_token', None)
            if access_token is not None:
                self.default_headers['Authorization'] = 'Bearer ' + access_token
            else:
                raise Exception('Access token not received from {}'.format(
                    self.request_url))

        except Exception as error:
            raise SwxApiClientException(
                'While getting token from Auth API: {}'.format(error)
            )
