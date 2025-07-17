# 베이스 이미지 설정
FROM python:3.9-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 패키지 업데이트 및 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# requirements.txt 복사 및 라이브러리 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Gunicorn 서버 실행
# Cloud Run이 PORT 환경 변수를 자동으로 주입합니다.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
