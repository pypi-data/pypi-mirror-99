from moocxing.plugins.sdk.AbstractPlugin import AbstractPlugin
import requests

class Plugin(AbstractPlugin):
    SLUG = "chat"

    def __init__(self, SKILL):
        super().__init__(SKILL)
        self.url = "https://api.naixing.vip/anonymous/wordManage/answers/"

        self.data = {
            "question": "",
            # "robotId": "4595",
            "robotId": "4485",
            "deviceId": ""
        }

    def handle(self, query):
        self.data["question"] = query.replace("chat","")

        info = requests.post(url=self.url, json=self.data).json()
        self.data["deviceId"] = info["data"]["deviceId"]

        print(f"\nanswers: {info['data']['answers']}")
        self.say(info['data']['answers'])


    def isValid(self, query):
        return "chat" in query
