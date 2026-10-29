import logging
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# [수정됨] 상대 경로 및 try-except 제거 (문제가 생기면 로그에서 즉시 확인 가능하도록 직관적인 import 사용)
from algorithms import run_all_sorts

# [필수 확인] FastAPI 인스턴스 생성 (이 코드가 없으면 서버가 시작되지 않음)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# [추가됨] Cloud Run 헬스 체크용 엔드포인트
@app.get("/")
def health_check():
    return {"status": "ok", "message": "Server is successfully running on Cloud Run"}

# ---------------------------------------------------------
# 아래부터는 기존에 작성하셨던 API 라우터(엔드포인트) 코드들을 
# 그대로 이어서 붙여넣어 주시면 됩니다.
# (예: @app.post("/sort") 등)
# ---------------------------------------------------------
