
"""
HTTP コールアウトを実施するクラス
"""

import requests
import urllib

class HTTPCallout:

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint # リクエスト先
        self.headers = {} # リクエストヘッダー
        self.bodies = {} # リクエストボディ
        self.timeout = (3.0, 5.0) # デフォルトのタイムアウト

    def _url_parameter_parser(self) -> list[any, any]:
        """
        URLとパラメーターの辞書を返す
        """
        pr = urllib.parse.urlparse(self.endpoint)
        return pr, urllib.parse.parse_qs(pr.query)

    def set_param(self, key: any, value: any) -> None:
        """
        URLのパラメータ設定
        """
        pr, d = self._url_parameter_parser()
        d[key] = value
        self.endpoint = urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))
    
    def set_params(self, params: dict) -> None:
        """
        URLのパラメータ設定
        """
        pr, d = self._url_parameter_parser()
        d = dict(**d, **params)
        self.endpoint = urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))

    def set_header(self, key: any, value: any) -> None:
        """
        リクエストヘッダーの設定
        """
        self.headers[key] = value
    
    def set_body(self, key: any, value: any) -> None:
        """
        リクエストボディの設定
        """
        self.bodies[key] = value

    def get(self) -> list[int, dict]:
        """
        HTTP Request GET
        """
        try:
            res = requests.get(url=self.endpoint, timeout=self.timeout)
        except Exception as e:
            print(f"Error: {e}")

        return res.status_code, res.json()
    
    def post(self) -> int:
        """
        HTTP Request POST
        """
        try:
            res = requests.post(url=self.endpoint, headers=self.headers, data=self.bodies, timeout=self.timeout)
        except Exception as e:
            print(f"Error: {e}")
        
        return res.status_code