from moocxing.robot import Constants
from moocxing.robot import Config   
import os
import logging

log = logging.getLogger(__name__)

version = "v0.7.4"

class MOOCXING:
    def __init__(self,config = None):
        logging.basicConfig(level=Config.get("loglevel"), format='[%(filename)s][%(levelname)s]: %(message)s')
    
    def getAllSkill(self):
        SKILL = {}
        # 初始化播放器和录音模块
        SKILL["media"] = self.initMedia()
        # 初始化MQTT模块
        SKILL["mqtt"] = self.initMqtt()
        # 初始化拼音模块
        SKILL["pinyin"] = self.initPinyin()
        # 初始化我的世界
        SKILL["mc"] = self.initMinecraft()
        # 初始化串口模块
        SKILL["serial"] = self.initSerial()
        # 初始化语音识别+语音合成模块
        SKILL["speech"] = self.initSpeech()
        # 初始化NLP模块
        SKILL["nlp"] = self.initNLP()

        return SKILL


    def initMqtt(self):
        from .MXMqtt import MXMqtt
        try:
            log.info(">>> 正在初始化MQTT模块")
            return MXMqtt()
        except:
            log.warning("xxx 初始化MQTT模块失败")

    def initMinecraft(self):
        from mcpi.minecraft import Minecraft
        try:
            log.info(">>> 正在初始化Minecraft模块")
            return Minecraft.create(Config.get("minecraft/host"), Config.get("minecraft/post"))
        except:
            log.warning("xxx 未检测到Minecraft服务器")

    def initNLP(self):
        from .MXNLP import MXNLP
        try:
            log.info(">>> 正在初始化自然语言分析模块")
            return MXNLP()
        except:
            log.warning("xxx 初始化初始化自然语言分析模块失败")

    def initSpeech(self):
        from .MXSpeech import MXSpeech
        try:
            log.info(">>> 正在初始化语音识别/合成模块")
            return MXSpeech()
        except:
            log.warning("xxx 初始化语音识别/合成模块失败")

    def initPinyin(self):
        from .MXPinyin import MXPinyin
        try:
            log.info(">>> 正在初始化拼音模块")
            return MXPinyin()
        except:
            log.warning("xxx 初始化拼音模块失败")

    def initMedia(self):
        from .MXMedia import MXMedia
        try:
            log.info(">>> 正在初始化播放器模块")
            return MXMedia()
        except:
            log.warning("xxx 初始化播放器模块失败")

    def initSerial(self, com=None, bps=9600):
        from .MXSerial import MXSerial
        try:
            log.info(">>> 正在初始化串口通信模块")

            if com is None:
                return MXSerial(MXSerial.getCom(-1), bps)
            else:
                return MXSerial(com, bps)
        except:
            log.warning("xxx 未检测到串口")
