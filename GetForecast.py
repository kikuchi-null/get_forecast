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

    def write_messege(self):
        """
        apiからjson形式でレスポンスを受け取る。
        レスポンスをもとにLINEのメッセージを作成する
        """
        data = self.access_to_openweathermap()
        weather = json.loads(data)

        weather = weather["daily"][0]
        message = f"""
        City: {self.CITY}

        Weather: {weather["weather"][0]["description"].title()}

        Humidity: {weather["humidity"]} %

        Temperature 
        Morning: {weather["temp"]["morn"]} ℃
        Day: {weather["temp"]["day"]} ℃
        Evening: {weather["temp"]["eve"]} ℃
        Night: {weather["temp"]["night"]} ℃

        Max Temperature: {weather["temp"]["max"]} ℃
        Min Temperature: {weather["temp"]["min"]} ℃
        """

        if int(weather["weather"][0]["id"]) != 800: # 800は"はれ"の意味
            message += "\nAttention! BAD WEATHER!"

        return message.replace("        ", "")

    def send_messege(self, token, line_url):
        self.token, self.line_url = token, line_url
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            message = self.write_messege()
            payload = {"message": message}
        except:
            payload = {"messege": "ERROR has occured!"}
            
        r = requests.post(self.line_url, headers=headers, data=payload)
        return r.status_code

if __name__ == "__main__":

    # ACCESS
    lat = XXXX
    lon = XXXX
    CITY = XXXX
    KEY = XXXX
    FORECAST_URL = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&units=metric&appid={KEY}'

    TOKEN = XXXX
    LINE_URL = XXXX

    weather_forecast = GetForecast(CITY, FORECAST_URL)
    weather_forecast.send_messege(TOKEN, LINE_URL)
    
