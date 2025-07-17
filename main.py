import os
import gspread
import json  # json 라이브러리를 추가합니다.
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2.service_account import Credentials

# Flask 앱 초기화 및 CORS 설정
app = Flask(__name__)
CORS(app) # 모든 도메인에서의 요청을 허용 (개발용)

# --- ✨ 여기가 수정된 부분입니다 ✨ ---
# 구글 시트 인증 설정
scopes = ["https://www.googleapis.com/auth/spreadsheets"]

# 환경 변수에서 JSON 키 '문자열'을 가져옵니다.
key_string = os.environ.get("GCP_SA_KEY")

# 가져온 문자열을 파이썬 딕셔너리 형태로 변환합니다.
key_info = json.loads(key_string)

# 변환된 정보를 사용해 인증합니다.
creds = Credentials.from_service_account_info(
    info=key_info,  # eval() 대신 json.loads() 결과를 사용합니다.
    scopes=scopes
)
client = gspread.authorize(creds)
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
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
