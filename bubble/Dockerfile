# Python 3.11 슬림 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 목록 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# Gunicorn을 사용하여 앱 실행 (프로덕션 환경용 WSGI 서버)
# worker-tmp-dir을 메모리로 설정하여 성능 향상
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
