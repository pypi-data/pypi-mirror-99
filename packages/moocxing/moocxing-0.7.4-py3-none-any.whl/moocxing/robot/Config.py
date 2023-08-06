import yaml
from moocxing.robot import Constants
from moocxing.robot.utils import fileUtils
import logging
from os import path

log = logging.getLogger(__name__)

fileUtils.mkdir(Constants.STATIC_PATH)
fileUtils.mkdir(Constants.TEMP_PATH)
fileUtils.mkdir(Constants.CUSTOM_PLUGIN_PATH)
# fileUtils.mkdir(Constants.MUSIC_PATH)


DEFAULT = {
    'loglevel': 20,
    'mqtt': {'host': 'mqtt.16302.com', 'post': 1883},
    'minecraft': {'host': 'localhost', 'post': 4711}
}
fileUtils.mkFile(Constants.DEFAULT_CONFIG_PATH, DEFAULT)
fileUtils.mkFile(Constants.CUSTOM_CONFIG_PATH)

allConfig = {}
for path in [Constants.DEFAULT_CONFIG_PATH, Constants.CUSTOM_CONFIG_PATH]:
    with open(path) as f:
        if data := yaml.safe_load(f):
            allConfig.update(data)


def get(items):
    config = allConfig

    for item in items.split("/"):
        config = config.get(item)

    if config:
        return config
    else:
        log.warning(f"参数不存在：配置文件中没有找到{items}参数")
