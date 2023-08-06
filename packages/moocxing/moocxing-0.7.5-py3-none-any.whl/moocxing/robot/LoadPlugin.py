import pkgutil
from moocxing.robot import Constants

import logging

log = logging.getLogger(__name__)

def loadPlugin(SKILL):
    plugins = []
    locations = [
        Constants.PLUGIN_PATH,
        Constants.CUSTOM_PLUGIN_PATH
    ]

    for finder, name, ispkg in pkgutil.walk_packages(locations):
        loader = finder.find_module(name)

        mod = loader.load_module(name)

        if not hasattr(mod, 'Plugin'):
            continue

        plugin = mod.Plugin(SKILL)

        if plugin in plugins:
            continue

        if plugin.SLUG == "chat":
            chat = plugin
        else:
            plugins.append(plugin)

        log.info(f"{plugin.SLUG} 插件加载成功")

    return plugins,chat
