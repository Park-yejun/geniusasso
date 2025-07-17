import os
import gspread
from flask import Flask, request, jsonify
from flask_cors import CORS
# ✨ google.oauth2.service_account 와 json 라이브러리가 더 이상 필요 없습니다.

# Flask 앱 초기화 및 CORS 설정
app = Flask(__name__)
CORS(app)

# --- ✨ 여기가 수정된 부분입니다 ✨ ---
# Cloud Run 환경에서는 gspread가 자동으로 서비스 계정을 찾아 인증합니다.
# 따라서 복잡한 인증 코드 전체가 필요 없어집니다.
client = gspread.service_account()
# --- ✨ 수정된 부분 끝 ---


# 구글 시트 정보
SPREADSHEET_ID = '1F4rZbcBiuM9MDoFyfHnXVIFJ7GX99lUmaZZL_i3WZ40'
SHEET_NAME = '시트2'

@app.route('/update-sheet', methods=['POST'])
def update_sheet():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "Missing 'text' in request"}), 400

        text_to_write = data['text']

        # 시트 열고 데이터 쓰기
        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet(SHEET_NAME)
        sheet.update_acell('A1', text_to_write)

        return jsonify({"status": "success", "message": f"'{text_to_write}' written to Sheet2 A1"}), 200

    except Exception as e:
        # 오류 발생 시 로그에 더 자세히 출력
        app.logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# / 경로에 대한 기본 응답 추가 (서버 동작 확인용)
@app.route('/')
def index():
    return "Backend server is running!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
