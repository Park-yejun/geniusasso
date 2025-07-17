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
# ✨✨✨ 여기가 최종 수정된 부분입니다! 작업자(workers)를 2명으로 늘렸습니다. ✨✨✨
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "main:app"]
