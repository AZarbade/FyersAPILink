import os
import time
import base64
import datetime
import requests
from fyers_apiv3 import fyersModel
from urllib.parse import parse_qs, urlparse


class Fyers:
    API_BASE_URL = "https://api-t2.fyers.in/vagator/v2/"
    TOKEN_URL = "https://api-t1.fyers.in/api/v3/token"
    LOG_PATH = os.path.join(os.getcwd(), "logs/")

    def __init__(self, user_details: dict) -> None:
        # self.pin = pin
        # self.totp = totp
        self.username = user_details['username']
        self.client_id = user_details['client_id']
        self.redirect_uri = user_details['redirect_uri']
        self.secret_key = user_details['secret_key']
        self.session = requests.Session()

    def send_login_otp(self):
        url = self.API_BASE_URL + "send_login_otp_v2"
        res = self.session.post(url, json={"fy_id": self.get_encoded_string(self.username), "app_id": "2"}).json()
        return res

    def verify_otp(self, request_key, totp):
        url = self.API_BASE_URL + "verify_otp"
        payload = {"request_key": request_key, "otp": totp}
        res = self.session.post(url, json=payload).json()
        return res

    def verify_pin(self, request_key, pin: int):
        url = self.API_BASE_URL + "verify_pin_v2"
        payload = {"request_key": request_key, "identity_type": "pin", "identifier": self.get_encoded_string(pin)}
        res = self.session.post(url, json=payload).json()
        return res

    def get_encoded_string(self, string):
        base64_bytes = base64.b64encode(string.encode("ascii"))
        return base64_bytes.decode("ascii")

    def get_access_token(self, pin: int, totp: int):
        login_otp_response = self.send_login_otp()
        request_key = login_otp_response["request_key"]

        if datetime.datetime.now().second % 30 > 27:
            time.sleep(5)

        otp_verification_response = self.verify_otp(request_key, totp)
        pin_verification_response = self.verify_pin(otp_verification_response["request_key"], pin=pin)

        self.session.headers.update({"authorization": f"Bearer {pin_verification_response['data']['access_token']}"})

        payload = {
            "fyers_id": self.username,
            "app_id": self.client_id[:-4],
            "redirect_uri": self.redirect_uri,
            "appType": "100",
            "code_challenge": "",
            "state": "None",
            "scope": "",
            "nonce": "",
            "response_type": "code",
            "create_cookie": True,
        }

        token_response = self.session.post(url=self.TOKEN_URL, json=payload).json()

        if 'Url' in token_response:
            auth_code = parse_qs(urlparse(token_response['Url']).query)['auth_code'][0]
            return auth_code

        return token_response

    def start_session(self, pin: int, totp: int):
        auth_code = self.get_access_token(pin=pin, totp=totp)
        session = fyersModel.SessionModel(
            client_id=self.client_id,
            secret_key=self.secret_key,
            redirect_uri=self.redirect_uri,
            response_type="code",
            grant_type="authorization_code")

        session.set_token(auth_code)
        response = session.generate_token()
        access_token = response["access_token"]

        with open("access_token.txt", "w") as f:
            f.write(access_token)

    def start_client(self):
        with open("access_token.txt", "r") as f:
            access_token = f.read()

        client = fyersModel.FyersModel(
            token=access_token,
            log_path=self.LOG_PATH,
            client_id=self.client_id)
        
        return client
