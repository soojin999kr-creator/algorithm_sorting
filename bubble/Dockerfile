# 파이썬 가벼운 공식 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 파이썬이 바이트코드 파일을 만들지 않고 로그 출력을 버퍼링하지 않도록 설정
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 시스템 필수 패키지 설치
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 보안을 위한 권한 없는 사용자 생성 및 적용
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Cloud Run용 포트 설정
ENV PORT=8080
EXPOSE 8080

# Gunicorn을 사용해 프로덕션 서버 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--threads", "4", "--timeout", "0", "main:app"]
