import os
import gspread
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.oauth2.service_account import Credentials

# Flask 앱 초기화 및 CORS 설정
app = Flask(__name__)
CORS(app) # 모든 도메인에서의 요청을 허용 (개발용)

# 구글 시트 인증 설정
# GitHub Actions Secret에서 받아온 서비스 계정 정보를 사용
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
# 로컬 테스트 시: creds = Credentials.from_service_account_file('your-key-file.json', scopes=scopes)
# Cloud Run 환경에서는 환경 변수에서 직접 로드하는 것이 더 안전하지만,
# 이 예제에서는 GitHub Secret을 통해 전달된 내용을 사용합니다.
# 실제로는 Cloud Run의 환경 변수 기능을 사용하는 것을 권장합니다.
# 여기서는 gspread의 기본 인증 방식을 활용합니다.
# gspread는 GOOGLE_APPLICATION_CREDENTIALS 환경 변수를 자동으로 찾습니다.
creds = Credentials.from_service_account_info(
    info=eval(os.environ.get("GCP_SA_KEY")), # 환경 변수에서 키 정보 로드
    scopes=scopes
)
client = gspread.authorize(creds)

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
