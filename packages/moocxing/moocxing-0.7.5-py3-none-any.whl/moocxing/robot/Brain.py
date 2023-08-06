from moocxing.robot import LoadPlugin
from moocxing.robot import Constants
from threading import Thread

class Brain():
    def __init__(self, SKILL):
        self.plugins, self.chat = LoadPlugin.loadPlugin(SKILL)

    def query(self, text):
        for plugin in self.plugins:
            if not plugin.isValid(text):
                continue
            if plugin.IS_IMMERSIVE:
                Thread(target = plugin.handle,args = (text,)).start()
            else:
                plugin.handle(text)
            return True
        self.chat.handle("chat" + text)
        return False
