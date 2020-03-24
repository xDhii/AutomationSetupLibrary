from ExtendedRequestsLibrary import ExtendedRequestsLibrary
from robot.libraries.BuiltIn import BuiltIn
from .keywordgroup import KeywordGroup

class _S1api(KeywordGroup):

    def __init__(self):
        self.builtin = BuiltIn()
        self.extrequest = ExtendedRequestsLibrary()

    def __login_s1(self, base_url, user):
        headers = {"Content-Type": "application/json"}
        self.extrequest.create_session('s1_auth_api', base_url)
        resp = self.extrequest.post_request('s1_auth_api', '/iam/login', headers=headers, data=user)
        if resp.status_code != 200:
              self.builtin.fail("There was an error initializing session. Error was {}".format(resp.content))
        platform_jwt = 'Bearer ' + resp.headers['platform-token']
        return platform_jwt

    def generate_platform_token(self, base_url, user):
        """Initializes session in S1 platform and returns platform token.

        Arguments:
            - url: The server base URL of S1 login.
            - user: User credentials. It should be like {"username":"username","password":"value"}

        Example:
        | ${platform} | Generate Platform Token | base_url=${s1_auth_url} | user=${user}|

        """
        return self.__login_s1(base_url, user)

    def generate_internal_jwt(self, auth_url, authz_url, user, appid):
        """Initializes session in S1 platform, authorize platform token and return internal token.

        Arguments:
            - auth_url: The server base URL of S1 Login.
            - authz_url: The server base URL of S1 Authorization.
            - user: User credentials. It should be like {"username":"username","password":"value"}
        
        Example:
        | ${internal} | Generate Internal Jwt | auth_url=${s1_auth_url} | authz_url=${s1_authz_url} | user=${user}|

        """
        platform_token = self.__login_s1(auth_url, user)
        headers = {"Content-Type": "application/json", "Authorization":platform_token, "x-app-id":appid}
        self.extrequest.create_session('s1_authz_api', authz_url)
        resp = self.extrequest.post_request('s1_authz_api', '/iam/authz', headers=headers, data="{}")
        if resp.status_code != 200:
              self.builtin.fail("There was an error initializing session. Error was {}".format(resp.content))
        internal_jwt = 'Bearer ' + resp.headers['Authorization']
        return internal_jwt
