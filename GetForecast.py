import requests
import json


class GetForecast:

    def __init__(self, city, forecast_url):
        self.CITY, self.URL = city, forecast_url

    def access_to_openweathermap(self):
        """
        openwathermap apiへのアクセスをおこなう
        """
        response = requests.get(self.URL)
        forecast = response.text

        return forecast

    def create_message(self):
        """
        apiからjson形式でレスポンスを受け取る。
        レスポンスをもとにLINEのメッセージを作成する
        """
        data = self.access_to_openweathermap()
        weather = json.loads(data)["daily"][0]
        print(weather)

        warning_message = ""
        if int(weather["weather"][0]["id"]) != 800: # 800は"はれ"の意味
            warning_message = "\n注意! 悪天候!\n"
        
        detail_message = f"""
        場所: {self.CITY}
        天気: {weather["weather"][0]["description"].title()}
        湿度: {weather["humidity"]} %

        【気温】 
        朝: {weather["temp"]["morn"]} ℃
        昼: {weather["temp"]["day"]} ℃
        夕: {weather["temp"]["eve"]} ℃
        晩: {weather["temp"]["night"]} ℃

        最高: {weather["temp"]["max"]} ℃
        最低: {weather["temp"]["min"]} ℃
        """.replace("        ", "")

        print(warning_message + detail_message)

        return warning_message + detail_message

    def send_messege(self, token, line_url):
        self.token, self.line_url = token, line_url
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            message = self.create_message()
            payload = {"message": message}
        except:
            payload = {"messege": "ERROR has occured!"}
            
        r = requests.post(self.line_url, headers=headers, data=payload)
        return r.status_code

if __name__ == "__main__":

    # ACCESS
    lat = "XXXX"
    lon = "XXXX"
    CITY = "XXXX"
    KEY = "XXXX"
    FORECAST_URL = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={KEY}"

    TOKEN = "XXXX"
    LINE_URL = "XXXX"

    weather_forecast = GetForecast(CITY, FORECAST_URL)
    weather_forecast.send_messege(TOKEN, LINE_URL)
    
