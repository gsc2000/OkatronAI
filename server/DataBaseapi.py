"""ファイル操作"""

import os
import sys

import yaml

def readConfig(path):
    with open(path) as file:
        config = yaml.safe_load(file.read())
    return config

def writeConfig():
    pass