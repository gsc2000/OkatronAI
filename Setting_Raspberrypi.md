# ラズパイのセッティングについてメモ

# システムの更新
```
sudo apt update
sudo apt upgrade -y
```
# 日本語キーボード入力
下記サイトを参考
```
https://qiita.com/sukinasaki/items/426068d6e87169fa3d88
```

# IPの固定
```
https://chigusa-web.com/blog/%E3%83%A9%E3%82%BA%E3%83%91%E3%82%A4%E3%81%AEwi-fi%E8%A8%AD%E5%AE%9A%E3%81%A8%E5%9B%BA%E5%AE%9Aip%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%82%92%E8%A8%AD%E5%AE%9A%E3%81%99%E3%82%8B/
```

# SSHの設定
## SSHを設定する
```
デスクトップのスタートメニューから「設定」→「Raspberry Pi の設定」を選択。
「インターフェイス」タブの「VNC」「SSH」を「有効」にして「OK」を押します。
```

## SSHキーを生成する
```
cd /home/<username> # ディレクトリ移動
mkdir .ssh # ディレクトリの作成
ssh-keygen # SSHキーの生成
cat id_rsa.pub # 生成された公開鍵を確認
```

# Gitのインストール
```
sudo apt install git
```

# Pyenvのインストール Pythonのバージョン管理ツール
## 必要なライブラリをインストール
```
sudo apt install -y build-essential libffi-dev libssl-dev zlib1g-dev \
liblzma-dev libbz2-dev libreadline-dev libsqlite3-dev \
libopencv-dev tk-dev
```
## pyenv本体のダウンロードとインストール
```
cd /home/<username>
git clone https://github.com/pyenv/pyenv.git .pyenv
```

## .bashrcの更新
```
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
source ~/.bashrc
```

## pyenvがインストールできたかを確認
```
pyenv -v
```

## pythonのインストール
ラズパイのシステムPythonが3.9.2なので念のため、3.8にしておく
```
pyenv install 3.8.16
pyenv versions # インストール済みのpyenvのバージョンを確認できる
```

## pythonのバージョン設定追加
pyenvのグローバル設定をすることで特定のバージョンを呼び出せる？
```
pyenv global 3.8.16
```
下記コマンドを入力し、インストールしたバージョンが表示されればOK
```
python3.8 -V
-> Python 3.8.16
```