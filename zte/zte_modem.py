import requests
from urllib.parse import urlencode
from requests.models import PreparedRequest
import base64


def base64_encode(string: str) -> str:
    """
    Base64 encoding function to UTF-8 string
    """
    return str(base64.b64encode(bytes(string, 'utf-8')), encoding='utf-8')


def generate_request_url(url: str, params: dict[str, str]) -> str:
    req = PreparedRequest()
    req.prepare_url(url, params)
    return req.url


def fromHex(text: str):
    res=''
    for i in range(4,len(text),4):
        res += chr(int(text[i-4:i],16))
    return res



class ZTEModem:

    def __init__(self):
        self.ip = "192.168.0.1"
        self.command_get_ip = f"http://{self.ip}/goform/goform_get_cmd_process"
        self.command_set_ip = f"http://{self.ip}/goform/goform_set_cmd_process"
        self.password = "admin"
        self.stok_cookie = None
        self.modem_headers = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "dnt": "1",
            "sec-gpc": "1",
            "Referer": f"http://{self.ip}/index.html"
        }

    def auth(self) -> dict[str, str]:
        """
        Returns cookie (stok) for authentication. While "apply" equals True, stok applies locale.
        """
        answer = requests.post(
            self.command_get_ip,
            data = {
                'isTest': 'false',
                'goformId': 'LOGIN',
                'password': base64_encode(self.password)
            },
            headers = self.modem_headers | {
            "Origin": f"http://{self.ip}",
            }
        )
        if answer.json()['result'] != "0":
            raise Exception("Auth Error")
        self.stok_cookie = {"stok": answer.cookies.get("stok")}

    def list_sms(self) -> list[dict]:
        params = {
            "isTest": 'false',
            'cmd': 'sms_data_total',
            'page': '0',
            'data_per_page': '500',
            'mem_store': '1',
            'tags': '10'
        }
        url = generate_request_url(self.command_get_ip, params)
        url += '&order_by=order+by+id+desc'

        answer = requests.get(url,
            headers = self.modem_headers,
            cookies=self.stok_cookie
        )
        
        messages = answer.json()['messages']
        
        for message in messages:
            message['content'] = fromHex(message['content'])

        return messages

    def delete_sms(self, sms: dict):
        content = {
            "msg_id": sms["id"]
        }

        options = {
            "goformId": "DELETE_SMS",
            "IsTest": False,
            **content
        }
        search = urlencode(options)

        response = requests.post(self.command_set_ip, data=search, headers=self.modem_headers, cookies=self.stok_cookie)
        return response.json()

    def get_and_delete_sms(self):
        # Auth
        self.auth()
        # List
        sms = self.list_sms()

        for s in sms:
            try:
                self.delete_sms(s)
            except Exception:
                print("Failed to delete sms", s)

        return sms
