import os
import yaml

def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def mkFile(path,data = None):
    if not os.path.isfile(path):
        f = open(path, "w")
        yaml.dump(data,f)
        f.close()

