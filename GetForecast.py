import requests
import urllib

class HTTPCallout:

    def __init__(self, endpoint) -> None:
        self.endpoint = endpoint # リクエスト先
        self.params = {} # URLパラメーター
        self.headers = {} # リクエストヘッダー
        self.bodies = {} # リクエストボディ
        self.timeout = (3.0, 5.0) # デフォルトのタイムアウト

    def _url_parameter_parser(self):
        """
        URLとパラメーターの辞書を返す
        """
        pr = urllib.parse.urlparse(self.endpoint)
        return pr, urllib.parse.parse_qs(pr.query)

    def set_param(self, key, value) -> None:
        """
        URLのパラメータ設定
        """
        pr, d = self._url_parameter_parser()
        d[key] = value
        self.endpoint = urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))
    
    def set_params(self, params) -> None:
        """
        URLのパラメータ設定
        """
        pr, d = self._url_parameter_parser()
        d = dict(**d, **params)
        self.endpoint = urllib.parse.urlunparse(pr._replace(query=urllib.parse.urlencode(d, doseq=True)))

    def set_header(self, key, value):
        """
        リクエストヘッダーの設定
        """
        self.headers[key] = value
    
    def set_body(self, key, value):
        """
        リクエストボディの設定
        """
        self.bodies[key] = value

    def get(self):
        """
        HTTP Request GET
        """
        try:
            res = requests.get(url=self.endpoint, timeout=self.timeout)
        except Exception as e:
            print(f"Error: {e}")

        return res.status_code, res.json()
    
    def post(self):
        """
        HTTP Request POST
        """
        try:
            res = requests.post(url=self.endpoint, headers=self.headers, data=self.bodies, timeout=self.timeout)
        except Exception as e:
            print(f"Error: {e}")
        
        return res.status_code

class MessageUtil:

    def __init__(self, data) -> None:
        self.message = "" # 生成するメッセージ
        self.additional_message = "" # 追加データを用いて生成するメッセージ
        self.data = data # メッセージを生成するもととなるデータ

    def get_message(self):
        """
        送信するメッセージを生成して返す
        """
        self._add_warning()

        if len(self.additional_message) > 0:
            self.message += self.additional_message

        self._add_body()

        return self.message
    
    def _add_warning(self):
        """
        警告メッセージの生成
        """
        if int(self.data["weather"][0]["id"]) != 800: 
            # 800(晴れ)以外のときは警告文を生成する
            self.message += "\n注意! 悪天候!\n"

    def add_message(self, key, value):
        """
        追加メッセージの生成
        """
        # 引数のデータを参照してメッセージを追加する
        self.additional_message += f"\n{key}: {value}"

    def _add_body(self):
        """
        本文の生成
        """
        # 天気予報のデータをもとに本文を生成する
        self.message += f"""
        天気: {self.data["weather"][0]["description"]}
        湿度: {self.data["humidity"]} %

        【気温】 
        朝: {self.data["temp"]["morn"]} ℃
        昼: {self.data["temp"]["day"]} ℃
        夕: {self.data["temp"]["eve"]} ℃
        晩: {self.data["temp"]["night"]} ℃

        最高: {self.data["temp"]["max"]} ℃
        最低: {self.data["temp"]["min"]} ℃""".replace("        ", "")
