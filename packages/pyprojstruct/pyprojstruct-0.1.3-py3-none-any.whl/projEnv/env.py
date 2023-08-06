import sys
import os


def addEnvDirs(envKey: str, warning=False):
    paths = os.getenv(envKey)
    if not paths:
        if warning:
            print('addEnvDirs not find env key:{}'.format(envKey))
        return
    pathls = paths.split(';')
    for aDir in pathls:
        if os.path.exists(aDir):
            sys.path.append(aDir)
        else:
            print('addEnvDirs not find path:{}'.format(aDir))
