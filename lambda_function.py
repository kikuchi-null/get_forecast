# エンドポイント、郵便番号、APIキーは別ファイルで管理する
# 上記の情報はgitのバージョン管理の対象外
import json
from lambda_function_handler import HTTPCallout, MessageUtil
from constants import HEART_RAILS_GEO, POSTCODE, OPEN_WEATHER_MAP, OPEN_WEATHER_MAP_KEY, LINE, LINE_TOKEN 

def lambda_handler(event, context):

    """
    現在地の取得
    """
    location = HTTPCallout(HEART_RAILS_GEO) # https://geoapi.heartrails.com/api/json
    
    # パラメータ設定
    params  = {
        "method": "searchByPostal",
        "postal": POSTCODE,
    }
    location.set_params(params)
    print("Endpoint", location.endpoint)

    # コールアウト
    status_code, location_data = location.get()
    print("Status Code:", status_code)

    # レスポンスの処理
    city_town = location_data["response"]["location"][0]["city"] + location_data["response"]["location"][0]["town"] # 市区町村

    """
    天気予報の取得
    """
    forecast = HTTPCallout(OPEN_WEATHER_MAP) # https://api.openweathermap.org/data/2.5/onecall

    # パラメーター設定
    params = {
        "lat": location_data["response"]["location"][0]["y"], # 緯度
        "lon": location_data["response"]["location"][0]["x"], # 経度
        "appid": OPEN_WEATHER_MAP_KEY,
        "units": "metric",
        "lang": "ja",
    }
    forecast.set_params(params)
    print("Endpoint:", forecast.endpoint)

    # コールアウト
    status_code, weather_data = forecast.get()
    print("Status Code:", status_code)

    # レスポンスの処理
    weather_data = weather_data["daily"][0]

    """
    LINE送信
    """
    mu = MessageUtil(weather_data)
    line = HTTPCallout(LINE) # https://notify-api.line.me/api/notify

    # メッセージ作成
    mu.add_message("場所", city_town)
    message = mu.get_message()

    # リクエストヘッダー・ボディ設定
    line.set_header("Authorization", f"Bearer {LINE_TOKEN}")
    line.set_body("message", message)
    print("Endpoint:", line.endpoint)
    print("Header:", line.headers)
    print("Body:", line.bodies)

    # コールアウト
    status_code = line.post()
    print("Status Code:", status_code)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

if __name__ == "__main__":
    rtn = lambda_handler("", "")