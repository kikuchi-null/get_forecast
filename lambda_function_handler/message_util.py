"""
LINE メッセージを生成するクラス
"""

class MessageUtil:

    def __init__(self, data: dict) -> None:
        self.message = "" # 生成するメッセージ
        self.additional_message = "" # 追加データを用いて生成するメッセージ
        self.data = data # メッセージを生成するもととなるデータ

    def get_message(self) -> str:
        """
        送信するメッセージを生成して返す
        """
        self._add_warning()

        if len(self.additional_message) > 0:
            self.message += self.additional_message

        self._add_body()

        return self.message
    
    def _add_warning(self) -> None:
        """
        警告メッセージの生成
        """
        if int(self.data["weather"][0]["id"]) != 800: 
            # 800(晴れ)以外のときは警告文を生成する
            self.message += "\n注意! 悪天候!\n"

    def add_message(self, key: any, value: any) -> None:
        """
        追加メッセージの生成
        """
        # 引数のデータを参照してメッセージを追加する
        self.additional_message += f"\n{key}: {value}"

    def _add_body(self) -> None:
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
