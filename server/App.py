
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

def main():
    """アプリを起動する"""
    args: argparse.Namespace = myArgParser()

    state: OkatronState = OkatronState(args.config)
    server: OkatronServer = OkatronServer(state)

    server.run()

if __name__ == "__main__":
    main()