"""ユーザからのリクエスト処理"""

import os
import sys

import enum

import asyncio

class UserReq(enum.Enum):
    """ユーザリクエストの種類"""
    START: str = "Start"
    STOP: str = "Stop"

class UserIO():
    """ユーザリクエストを処理"""
    def __init__(self) -> None:
        pass

    def recvMesse(self):
        """メッセージの取得"""
        pass