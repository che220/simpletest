import os, logging, json, requests
from inference_local.authorization import Authorization

logger = logging.getLogger(os.path.basename(__file__))

env_realms = {'dev' : 'e2e',
              'e2e' : 'e2e',
              'prf' : 'perf',
              'prod' : 'prod',
              'cperf' : 'perf',
              'cdev' : 'e2e'}

class MXSRequest:
    def __init__(self, env):
        self.env = env
        self.realm = env_realms[self.env]
        self.auth = None

    def request(self, model, data):
        # Build the URL
        url = 'https://modelexecution-{env}.api.anything.com/v1/{model}/1/predict'
        url = url.format(env=self.env, model=model)

        # Create a athorization header string
        if self.auth is None:
            self.auth = Authorization(self.env).get_header()
            logger.info('authorization: %s', self.auth)

        # Make sure the data is stringified
        if isinstance(data, dict):
            data = json.dumps(data)

        # Perform a post request against MXS
        response = requests.post(
            url=url,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': self.auth,
            },
        )

        # Check and return request
        assert response.status_code == 200, AssertionError(response.text)
        return response.text
