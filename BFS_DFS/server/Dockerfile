# Google Cloud Run 배포용 Python 3.11 Slim 이미지 사용
FROM python:3.11-slim

# 표준 출력 버퍼링 비활성화 및 환경변수 설정
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8080

WORKDIR /app

# 의존성 파일 복사 및 설치 (캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# Cloud Run 기본 포트 노출
EXPOSE 8080

# Cloud Run의 동적 PORT 환경변수를 바인딩하여 Uvicorn 실행
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}

