from __future__ import absolute_import

import json
import os
import yaml
import logging
import requests
from requests.auth import AuthBase
from typing import List, Dict


class AoaClient(object):
    def __init__(self, **kwargs):
        self.logger = logging.getLogger(__name__)
        self.project_id = None
        self.aoa_url = None
        self.s3_bucket = None

        self.session = requests.Session()
        self.__parse_aoa_config(**kwargs)

    def __parse_yaml(self, yaml_path: str):
        with open(yaml_path, "r") as handle:
            conf = yaml.safe_load(handle)
        self.__parse_kwargs(**conf)

    def __parse_kwargs(self, **kwargs):
        self.aoa_url = kwargs.get("aoa_url", self.aoa_url)

        if "auth_mode" in kwargs:
            auth_mode = kwargs["auth_mode"]
            if auth_mode == "basic":
                credentials = kwargs.get("auth_credentials", None)
                # backward compatibility for credentials key as was called aoa_credentials instead of auth_credentials
                if "aoa_credentials" in kwargs and credentials is None:
                    credentials = kwargs.get("aoa_credentials")

                self.__configure_basic_auth(credentials,
                                            kwargs.get("auth_user", None),
                                            kwargs.get("auth_pass", None))

            elif auth_mode == "kerberos":
                self.__configure_kerberos()

            elif auth_mode == "oauth":
                self.__configure_oauth_refresh_token(
                    kwargs.get("auth_client_id", None),
                    kwargs.get("auth_client_secret", None),
                    kwargs.get("auth_client_token_url", None),
                    kwargs.get("auth_client_refresh_token", None))

            else:
                raise Exception("Auth mode: {} not supported.".format(auth_mode))

        if "verify_connection" in kwargs:
            self.verify_aoa_connection = kwargs["verify_connection"]

    def __parse_env_variables(self):
        self.aoa_url = os.environ.get("AOA_URL", self.aoa_url)

        if "AOA_API_AUTH_MODE" in os.environ:
            auth_mode = os.environ.get("AOA_API_AUTH_MODE")

            if auth_mode == "basic":
                self.__configure_basic_auth(os.environ.get("AOA_API_AUTH_CREDENTIALS", None),
                                            os.environ.get("AOA_API_AUTH_USER", None),
                                            os.environ.get("AOA_API_AUTH_PASS", None))

            elif auth_mode == "kerberos":
                self.__configure_kerberos()

            elif auth_mode == "oauth":
                self.__configure_oauth_refresh_token(
                    os.environ.get("AOA_API_AUTH_CLIENT_ID", None),
                    os.environ.get("AOA_API_AUTH_CLIENT_SECRET", None),
                    os.environ.get("AOA_API_AUTH_TOKEN_URL", None),
                    os.environ.get("AOA_API_AUTH_REFRESH_TOKEN", None))

            else:
                raise Exception("Auth mode: {} not supported.".format(auth_mode))

    def __parse_aoa_config(self, **kwargs):
        if "config_file" in kwargs:
            self.__parse_yaml(kwargs['config_file'])
        else:
            from pathlib import Path
            config_file = "{}/.aoa/config.yaml".format(Path.home())
            if os.path.isfile(config_file):
                self.__parse_yaml(config_file)

        self.__parse_env_variables()
        self.__parse_kwargs(**kwargs)

    def set_project_id(self, project_id: str):
        """
        set project id

        Parameters:
           project_id (str): project id(uuid)
        """
        self.project_id = project_id

    def get_current_project(self):
        """
        get project id

        Return:
           project_id (str): project id(uuid)
        """
        return self.project_id

    def select_header_accept(self, accepts: List[str]):
        """
        converts list of header into a string

        Return:
            (str): request header
        """
        if not accepts:
            return
        accepts = [x.lower() for x in accepts]
        if 'application/json' in accepts:
            return 'application/json'
        else:
            return ', '.join(accepts)

    def get_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str]):
        """
        wrapper for get request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters

        Returns:
            dict for resources, str for errors, None for 404
        Raise:
            raises HTTPError in case of error status code other than 404
        """

        resp = self.session.get(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params
        )

        if resp.status_code == 404:
            return None

        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError:
            return resp.text

    def post_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str], body: Dict[str, str]):
        """
        wrapper for post request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """
        resp = self.session.post(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body)
        )

        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError:
            return resp.text

    def put_request(self, path, header_params: Dict[str, str], query_params: Dict[str, str], body: Dict[str, str]):
        """
        wrapper for put request

        Parameters:
           path (str): url
           header_params (dict): header parameters
           query_params (dict): query parameters
           body (dict): request body

        Returns:
            dict for resources, str for errors
        Raise:
            raises HTTPError in case of error status code
        """
        resp = self.session.put(
            url=self.__strip_url(self.aoa_url) + path,
            headers=header_params,
            params=query_params,
            data=json.dumps(body)
        )

        resp.raise_for_status()

        try:
            return resp.json()
        except ValueError:
            return resp.text

    def __strip_url(self, url):
        return url.rstrip('/')

    def __configure_basic_auth(self, credentials, username, password):
        if credentials is None and (username is None and password is None):
            raise Exception("credentials or (username, password) must be defined with auth_mode of 'basic'")

        from base64 import b64encode

        if credentials:
            self.session.auth = AoaAuth(credentials)

        else:
            self.session.auth = AoaAuth(b64encode("{}:{}".format(username, password).encode()).decode())

    def __configure_oauth_refresh_token(self, client_id, client_secret, token_url, refresh_token):
        if client_id is None or client_secret is None or token_url is None or refresh_token is None:
            raise Exception("client_id, client_secret, token_url and refresh_token must be defined "
                            "with auth_mode of 'oauth'")

        from requests_oauthlib import OAuth2Session
        from requests.auth import HTTPBasicAuth

        self.session = OAuth2Session(client_id=client_id)
        self.session.refresh_token(token_url=token_url, refresh_token=refresh_token,
                                   auth=HTTPBasicAuth(client_id, client_secret))

    def __configure_kerberos(self):
        from requests_kerberos import HTTPKerberosAuth, OPTIONAL
        self.session.auth = HTTPKerberosAuth(mutual_authentication=OPTIONAL)


class AoaAuth(AuthBase):
    def __init__(self, aoa_credentials):
        self.aoa_credentials = aoa_credentials

    def __call__(self, r):
        r.headers['Authorization'] = "Basic {}".format(self.aoa_credentials)
        return r
