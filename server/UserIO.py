"""ユーザからのリクエスト処理"""

import os
import sys

import enum
import json

import asyncio
import websockets as wb

class UserReq(enum.Enum):
    """ユーザリクエストの種類"""
    START: str = "Start"
    STOP: str = "Stop"

class UserIO():
    """ユーザリクエストを処理"""
    def __init__(self, sock) -> None:
        self.sock = sock

    async def recvMesse(self):
        """メッセージの取得"""
        command = await self.sock.recv()
        print(command)
        return json.loads(command)