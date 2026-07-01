import requests


class KISBroker:

    def __init__(self, app_key, app_secret, account_no, access_token=None):

        self.base_url = "https://openapi.koreainvestment.com:9443"

        self.app_key = app_key
        self.app_secret = app_secret
        self.account_no = account_no
        self.access_token = access_token

    # -----------------------------
    # TOKEN 발급
    # -----------------------------
    def get_token(self):

        url = f"{self.base_url}/oauth2/tokenP"

        data = {
            "grant_type": "client_credentials",
            "appkey": self.app_key,
            "appsecret": self.app_secret
        }

        res = requests.post(url, json=data)

        token = res.json().get("access_token")

        self.access_token = token

        return token

    # -----------------------------
    # BUY ORDER (현금매수)
    # -----------------------------
    def buy(self, ticker, qty):

        url = f"{self.base_url}/uapi/domestic-stock/v1/trading/order-cash"

        headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {self.access_token}",
            "appkey": self.app_key,
            "appsecret": self.app_secret,
            "tr_id": "TTTC0802U"
        }

        body = {
            "CANO": self.account_no,
            "ACNT_PRDT_CD": "01",
            "PDNO": ticker,
            "ORD_DVSN": "01",
            "ORD_QTY": str(qty),
            "ORD_UNPR": "0"
        }

        res = requests.post(url, json=body, headers=headers)

        return res.json()