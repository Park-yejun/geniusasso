from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    # 구글 시트 연동 없이, 오직 이 메시지만 반환합니다.
    return "Hello World! The basic server is running correctly."

if __name__ == "__main__":
    # Gunicorn이 이 파일을 실행하므로, 이 부분은 로컬 테스트용입니다.
    app.run(host='0.0.0.0', port=8080)
