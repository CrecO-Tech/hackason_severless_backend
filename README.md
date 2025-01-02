# かシャッタ採点 serverless-function

- serverlss fremework(python)を利用して、かシャッタ採点機能をサーバレスで処理を行う

# 初期設定

1. python の version を 3.10 系にする
2. 仮想環境に入る

```bash
# 仮想環境の作成
python -m venv .venv
# 仮想環境に入る
source venv/bin/activate
```

3. ライブラリーのインストール

```bash
pip install -r requirements.txt
```

# ローカル環境の構築方法

```bash
sls offline start
```

# デプロイ方法

https://github.com/nagisa599/serverless-fremework-v4-explain
