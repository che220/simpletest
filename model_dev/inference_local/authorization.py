import os, json, requests, logging

logger = logging.getLogger(os.path.basename(__file__))

class Authorization:
    def __init__(self, env):
        self.env = env

    def get_header(self):
        """Build the authorization header value for a specific environment"""

        # Create an account
        appid, secret = self._get_appid_and_secret()
        userid, ticket = self._get_userid_and_ticket()

        authorization = (
            'IAM_Authentication '
            'appid={appid},'
            'app_secret={app_secret},'
            'token_type=IAM-Ticket,'
            'userid={userid},'
            'token={token}'
        ).format(
            appid=appid,
            app_secret=secret,
            userid=userid,
            token=ticket,
        )
        return authorization

    def _get_userid_and_ticket(self):
        '''
        get test userid and ticket

        :return:
        '''
        response = requests.post(
            url='https://accts-e2e.platform.net/v1/iamtickets/sign_in',
            data=json.dumps({
                "username": "iamt73",
                "password": "1231231231"
            }),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'authorization' : 'IAM_Authentication appid=platform.kodiak.ds,app_secret= preprdVEO84PX6yGlBZYGv7N',
                'cache-control' : 'no-cache',
                'originatingip' : '1.2.3.4'
            }
        )

        # Check results
        assert response.status_code == 200, AssertionError(response.text)

        # Extract response information
        payload = response.json()
        userid = payload['iamTicket']['userId']
        ticket = payload['iamTicket']['ticket']
        return userid, ticket

    def _get_appid_and_secret(self):
        if self.env == 'cdev':
            return 'cbt-test-user', 'preprdQwwyL9DGqBhq6'
        return 'ml-cbt-test-user', 'prepbzQwwyL9DGqBhq6'
