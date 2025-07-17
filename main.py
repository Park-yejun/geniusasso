import os
import gspread
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Cloud Run 환경에서는 gspread가 자동으로 서비스 계정을 찾아 인증합니다.
client = gspread.service_account()

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

        spreadsheet = client.open_by_key(SPREADSHEET_ID)
        sheet = spreadsheet.worksheet(SHEET_NAME)
        sheet.update_acell('A1', text_to_write)

        return jsonify({"status": "success", "message": f"'{text_to_write}' written to Sheet2 A1"}), 200

    except Exception as e:
        app.logger.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

# 서버 동작 확인용
@app.route('/')
def index():
    return "Backend server is running!"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
