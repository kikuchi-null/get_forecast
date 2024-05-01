import json
from GetForecast import HTTPCallout, MessageUtil
from constants import POSTCODE, OPEN_WEATHER_MAP_KEY, LINE_TOKEN

def lambda_handler(event, context):

    # ENDPOINT
    HEART_RAILS_GEO = "https://geoapi.heartrails.com/api/json" # https://geoapi.heartrails.com/
    OPEN_WEATHER_MAP = "https://api.openweathermap.org/data/2.5/onecall" # https://openweathermap.org/forecast5
    LINE = "https://notify-api.line.me/api/notify" # https://notify-bot.line.me/ja/

    """
    現在地の取得
    """
    postcode = HTTPCallout(HEART_RAILS_GEO)
    
    # パラメータ設定
    postcode.set_param("method", "searchByPostal")
    postcode.set_param("postal", POSTCODE)
    print("Endpoint", postcode.endpoint)

    # コールアウト
    status_code, location_data = postcode.get()
    print("Status Code:", status_code)

    # レスポンスの処理
    latitude = location_data["response"]["location"][0]["y"] # 緯度
    longtitude = location_data["response"]["location"][0]["x"] # 経度
    city_town = location_data["response"]["location"][0]["city"] + location_data["response"]["location"][0]["town"] # 市区町村

    """
    天気予報の取得
    """
    forecast = HTTPCallout(OPEN_WEATHER_MAP)

    # パラメーター設定
    forecast.set_param("lat", latitude)
    forecast.set_param("lon", longtitude)
    forecast.set_param("appid", OPEN_WEATHER_MAP_KEY)
    forecast.set_param("units", "metric")
    forecast.set_param("lang", "ja")
    print("Endpoint:", forecast.endpoint)

    # コールアウト
    status_code, weather_data = forecast.get()
    print("Status Code:", status_code)

    # レスポンスの処理
    weather_data = weather_data["daily"][0]

    """
    LINE送信
    """
    ms = MessageUtil(weather_data)
    line = HTTPCallout(LINE)

    # メッセージ作成
    ms.add_message("場所", city_town)
    message = ms.get_message()

    # コールアウト
    line.set_header("Authorization", f"Bearer {LINE_TOKEN}")
    line.set_body("message", message)
    line.post()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    rtn = lambda_handler("", "")