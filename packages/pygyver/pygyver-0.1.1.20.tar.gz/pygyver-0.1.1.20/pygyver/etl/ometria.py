"""
Ometria API
http://docs.ometria.com/apis/data_api_v2/

- the env vars for the authentication are stored on the kubernetes cluster
under 'ometria-access-credentials'
- functionality:
    api credentials
    send custom events
"""
import logging
import os
import requests


class OmetriaExecutor:
    """
    Ometria API handler.

    Args:
        prod_env: switch between prod and staging environment (default True),
            this changes the api keys OMETRIA_API_KEY / OMETRIA_STAGING_API_KEY

    Attributes:
        api_endpoint: the base API endpoint
        api_key: required for authentication
        api_headers: header to be included in the request
        payload: the formatted payload to be sent
        response: the response from the API call

    Returns:
        OmetriaExecutor object
    """

    def __init__(self, prod_env: bool = True):
        """
        Initiate and collect API credentials.
        """
        self.prod_env = prod_env
        self.api_endpoint = "https://api.ometria.com/v2"
        self.api_key = None
        self.api_headers = None
        self.payload = None
        self.response = None
        self.set_api_credentials()

    def set_api_credentials(self):
        """
        Collect API credentials depending on the environment.
        """
        # api key
        api_key_env_var = "OMETRIA_API_KEY"
        if not self.prod_env:
            api_key_env_var = "OMETRIA_STAGING_API_KEY"

        if api_key_env_var in os.environ:
            self.api_key = os.getenv(api_key_env_var)
            logging.info("API credentials set")
        else:
            raise KeyError(f"Env var {api_key_env_var} does not exist")

        # headers
        self.api_headers = {
            "X-Ometria-Auth": self.api_key,
            "Content-Type": "application/json"
        }

    def send_custom_events(self):
        """
        Send custom_event type of payload to Ometria, save the API response.
        """
        if self.payload:
            # check if payload length is valid - 100 items per send
            payload_len = len(self.payload)
            if payload_len <= 100:
                # request - not adding retry for POST request
                self.response = requests.post(
                    json=self.payload,
                    url=f"{self.api_endpoint}/push",
                    headers=self.api_headers
                )
                logging.info(f"Sent {payload_len} 'custom_events' items")
                self.payload = None

            else:
                raise ValueError(
                    f"Payload too big - {payload_len}, max 100 items"
                )
        else:
            logging.info("No send - empty payload")
