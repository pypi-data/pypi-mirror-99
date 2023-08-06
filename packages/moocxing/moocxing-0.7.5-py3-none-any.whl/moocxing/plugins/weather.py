import requests
from moocxing.plugins.sdk.AbstractPlugin import AbstractPlugin


class Plugin(AbstractPlugin):
    SLUG = "weather"

    def handle(self, query):
        city = self.nlp.getCity(query)

        url = "https://free-api.heweather.net/s6/weather?location=" + city + "&key=3bffba48276c408b9107e275a51f111e"
        res = requests.post(url)
        info = dict(res.json())
        try:
            nowInfo = info["HeWeather6"][0]["now"]
            lifeStyle = info["HeWeather6"][0]["lifestyle"]
            location = info["HeWeather6"][0]["basic"]["location"]

            tmp = nowInfo["tmp"]
            fl = nowInfo["fl"]
            cond = nowInfo["cond_txt"]
            windDir = nowInfo["wind_dir"]
            windSc = nowInfo["wind_sc"]
            hum = nowInfo["hum"]
            vis = nowInfo["vis"]
            airBrf = lifeStyle[7]["brf"]

            print("今天%s的天气状况：%s，温度：%s℃，体感温度：%s℃，空气质量：%s，风向：%s，风力：%s级，湿度：百分之%s，能见度：%s公里" % (
                location, cond, tmp, fl, airBrf, windDir, windSc, hum, vis))
            self.say("今天%s的天气状况：%s，温度：%s℃，体感温度：%s℃，空气质量：%s，风向：%s，风力：%s级，湿度：百分之%s，能见度：%s公里" % (
                location, cond, tmp, fl, airBrf, windDir, windSc, hum, vis))
        except:
            return "没有查到%s的天气" % city

    def isValid(self, query):
        return "天气" in query
