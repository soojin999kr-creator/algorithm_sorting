"""Google Cloud Run 배포용 FastAPI 서버 (main.py)

셸 정렬, 퀵 정렬, 병합 정렬의 상태 스냅샷 히스토리를 생성하여
클라이언트(웹 브라우저 및 Google Apps Script)에 제공하는 백엔드 API 서버입니다.
"""

import logging
import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

# 로컬 스냅샷 생성 모듈 임포트
try:
    from .algorithms import run_all_sorts
except ImportError:
    from algorithms import run_all_sorts

# 로깅 설정
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# FastAPI 애플리케이션 초기화
app = FastAPI(
    title="Algorithm Sorting Visualizer API",
    description="셸 정렬, 퀵 정렬, 병합 정렬의 상태 스냅샷을 스트리밍 재생용으로 제공하는 API",
    version="1.0.0",
)

# CORS (Cross-Origin Resource Sharing) 설정
# Google Apps Script 및 브라우저 클라이언트에서의 교차 출처 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 요청 데이터 모델 정의
class SortRequest(BaseModel):
    numbers: List[int] = Field(
        ...,
        description="정렬할 정수 리스트 (최소 2개, 최대 50개 권장)",
        example=[38, 27, 43, 3, 9, 82, 10],
    )

    @field_validator("numbers")
    @classmethod
    def validate_numbers(cls, v: List[int]) -> List[int]:
        if not v:
            raise ValueError("배열이 비어 있습니다. 최소 2개 이상의 정수를 입력해주세요.")
        if len(v) < 2:
            raise ValueError("정렬 비교를 위해 최소 2개 이상의 숫자가 필요합니다.")
        if len(v) > 60:
            raise ValueError(
                f"원활한 웹 애니메이션 재생을 위해 최대 60개 이하의 배열만 지원합니다. (현재: {len(v)}개)"
            )
        for num in v:
            if not (-10000 <= num <= 10000):
                raise ValueError(
                    f"숫자 값이 범위를 초과했습니다. (-10,000 ~ 10,000 사이 값만 허용, 입력값: {num})"
                )
        return v


@app.get("/", tags=["Health Check"])
def root():
    """서버 기본 상태 및 작동 확인 엔드포인트"""
    return {
        "status": "online",
        "service": "Algorithm Sorting Visualizer Backend (Cloud Run)",
        "supported_algorithms": ["Shell Sort", "Quick Sort", "Merge Sort"],
        "endpoints": {
            "health": "/health",
            "sort_api": "/api/sort (POST)",
        },
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """Cloud Run 헬스 체크용 엔드포인트"""
    return {"status": "healthy", "service": "sorting-api"}


@app.post("/api/sort", tags=["Sorting Algorithms"])
def sort_algorithms(request: SortRequest):
    """3가지 정렬 알고리즘(셸, 퀵, 병합)을 실행하고 각 스텝별 스냅샷 히스토리를 반환합니다.

    - **셸 정렬 (Shell Sort)**: 간격(Gap) 축소 및 서브그룹별 삽입 스냅샷
    - **퀵 정렬 (Quick Sort)**: 피벗(Pivot) 지정, 대소 비교 및 제자리 확정 스냅샷
    - **병합 정렬 (Merge Sort)**: 논리적 분할, 서브배열 병합 비교 및 원본 덮어쓰기 스냅샷
    """
    try:
        logger.info(f"정렬 요청 수신 - 배열 길이: {len(request.numbers)}, 데이터: {request.numbers}")
        result = run_all_sorts(request.numbers)
        return {
            "success": True,
            "message": "성공적으로 3가지 알고리즘의 스냅샷 히스토리가 생성되었습니다.",
            "data": result,
        }
    except Exception as e:
        logger.error(f"정렬 스냅샷 생성 중 예외 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 내부에서 알고리즘 스냅샷 처리 중 오류가 발생했습니다: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    # Cloud Run은 환경변수 PORT를 주입하므로 기본값 8080 사용
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"로컬 Uvicorn 서버 시작 - 포트: {port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)

