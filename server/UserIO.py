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
    def __init__(self) -> None:
        pass

    async def recvMesse(self):
        pass