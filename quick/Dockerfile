# ==============================================================================
# Google Cloud Run 배포용 Dockerfile
# Python 3.11 슬림 이미지를 기반으로 가볍고 빠른 컨테이너를 빌드합니다.
# ==============================================================================

# 베이스 이미지로 파이썬 슬림 버전 사용
FROM python:3.11-slim

# 표준 출력 버퍼링 비활성화 및 바이트코드 생성 최소화
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 컨테이너 내 작업 디렉토리 설정
WORKDIR /app

# 종속성 파일 복사 및 설치 (캐시 레이어 최적화)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 소스 코드 복사
COPY . .

# Cloud Run에서 기본적으로 제공하는 포트 8080 (환경변수 PORT 주입 지원)
ENV PORT=8080
EXPOSE 8080

# Uvicorn 서버 실행 (단일 프로세스 컨테이너)
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT}

