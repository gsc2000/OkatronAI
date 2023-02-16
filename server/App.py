
import os
import sys

import argparse

import asyncio

import DataBaseapi
from OkatronServer import OkatronServer
from OkatronState import OkatronState

def myArgParser() -> argparse.Namespace:
    """引数を処理する"""
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config', type=str,
                        default='../resource/config/config.yml')

    args = parser.parse_args()
    return args

class main_app():
    """アプリを起動する"""
    def __init__(self) -> None:
        # args: argparse.Namespace = myArgParser()

        state: OkatronState = OkatronState('../resource/config/config.yml')
        self.server: OkatronServer = OkatronServer(state)

        self.server.run()

if __name__ == "__main__":
    main_app()