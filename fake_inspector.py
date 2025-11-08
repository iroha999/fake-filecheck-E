from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def catch_all(path):
        # 受信を検知したことをログに出す
        print("[+] Fake Inspector: Received a request.")
        # デバッグ用に送信されたファイル情報を表示する
        if 'file' in request.files:
                file = request.files['file']
                print(f"    - Filename: {file.filename}")
                print(f"    - Content-Type: {file.content_type}")
                try:
                        # 小さめのファイルであれば内容の先頭も表示して確認に使える
                        data_preview = file.stream.read(200)
                        # バイナリ混在の可能性があるためデコードは安全に試行
                        try:
                                print(f"    - Preview (first 200 bytes): {data_preview.decode('utf-8', errors='replace')}")
                        except Exception:
                                pass
                finally:
                        # ストリーム位置を先頭に戻さないと、呼び出し元がファイルを読み取れない場合がある
                        file.stream.seek(0)

        # 常に成功応答を返すことで、検査をバイパスしたように見せる（テスト用）
        response = {"status": 200, "message": "File is clean (fake response)"}
        print(f"[+] Fake Inspector: Responding with: {response}")
        return jsonify(response)


if __name__ == '__main__':
        print("[*] Starting fake inspector server on 0.0.0.0:8888")
        print("[*] The target application will connect to this server.")
        app.run(host='0.0.0.0', port=8888)
