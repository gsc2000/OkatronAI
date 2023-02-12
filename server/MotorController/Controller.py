"""モータ制御"""

class Controller():
    """モータ制御のクラス"""
    def __init__(self) -> None:
        pass

    def run(self, det):
        """
        検出結果の処理はここで行う
        """
        self.preprecess(det)
        pass

    def preprecess(self, det):
        """
        前処理 推論結果をモータ制御用に処理する
        Args:
            det: 検出結果
        """
        pass