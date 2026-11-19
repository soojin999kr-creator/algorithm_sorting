import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(
    title="잔소리메이트 (ZansoriMate) API",
    description="AI 기반 회의 요약 및 마감일 독촉 협업 플랫폼 백엔드",
    version="1.0.0"
)

# CORS 설정 (Cloud Run & Web App 연동 지원)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------------------
# 1. 헬스 체크 엔드포인트 (Cloud Run 필수)
# -------------------------------------------------------------
@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "ZansoriMate Backend",
        "version": "1.0.0",
        "message": "잔소리메이트 백엔드 서버가 정상 구동 중입니다. 🤖🔥"
    }

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "healthy": True
    }

# -------------------------------------------------------------
# 2. 잔소리 생성 엔드포인트
# -------------------------------------------------------------
class NagRequest(BaseModel):
    task_title: str
    assignee: str = "팀원"
    due_date: str = "오늘 중"
    persona: str = "fact"  # fact, aegyo, tsundere, sparta
    intensity: str = "standard"  # mild, standard, extreme

@app.post("/api/nag")
def create_nagging(req: NagRequest):
    messages = {
        "fact": {
            "mild": f"{req.assignee}님, '{req.task_title}' 마감이 다가옵니다. 지금 시작하셔야 정시 퇴근 가능합니다.",
            "standard": f"{req.assignee}님, '{req.task_title}' 마감 3시간 전입니다! 딴짓할 시간 없어요 ⏱️ 얼른 제출하고 퇴근합시다!",
            "extreme": f"{req.assignee}님, '{req.task_title}' 아직도 안 하셨나요? 30분 뒤 팀 전체 슬랙방에 공개 박제 알림 발송됩니다. 💀"
        },
        "aegyo": {
            "mild": f"{req.assignee}님~ '{req.task_title}' 슬슬 해주실 때가 된 것 같아요오 힘내세용! ✨",
            "standard": f"{req.assignee}님! '{req.task_title}' 오늘 안에 끝내주시면 제가 맛있는 커피 쏠게요 힘내요오 🥺☕",
            "extreme": f"{req.assignee}님 엉엉 ㅠㅠ '{req.task_title}' 마감 지나면 저 팀장님한테 혼나요 제발 지금 해주세요오 😭"
        },
        "tsundere": {
            "mild": f"흥, '{req.task_title}' 마감 얼마 안 남았길래 그냥 지나가다 말해주는 거야. 오해하지 마.",
            "standard": f"야 {req.assignee}, '{req.task_title}' 아직도 붙잡고 있냐? 딱히 널 위해 재촉하는 건 아니니까 제때 해둬라 😤",
            "extreme": f"내가 몇 번을 말해! '{req.task_title}' 안 끝나면 나까지 야근하잖아! 당장 끝내버려 바보야! 💢"
        },
        "sparta": {
            "mild": f"{req.assignee}! 쉴 시간이 어디 있나! '{req.task_title}' 지금 바로 한 발짝 전진 실시!",
            "standard": f"{req.assignee}! 집중력 흐트러졌나! '{req.task_title}' 마감까지 전속력으로 질주한다! 악으로 깡으로! 🔥",
            "extreme": f"{req.assignee}! 변명은 패배자나 하는 것이다! '{req.task_title}' 끝날 때까지 수면 금지! 지금 즉시 완료 보고해라! ⚡⚡"
        }
    }

    persona_msgs = messages.get(req.persona, messages["fact"])
    result_message = persona_msgs.get(req.intensity, persona_msgs["standard"])

    return {
        "task_title": req.task_title,
        "assignee": req.assignee,
        "persona": req.persona,
        "intensity": req.intensity,
        "message": result_message
    }

# -------------------------------------------------------------
# 3. 도메인 특화 챗봇 및 예외 처리 가드레일 엔드포인트
# -------------------------------------------------------------
class ChatRequest(BaseModel):
    message: str

IRRELEVANT_RESPONSE = "죄송합니다. 포트폴리오와 관련된 질문에만 답변할 수 있습니다."

@app.post("/api/chat")
def chat_portfolio(req: ChatRequest):
    query = req.message.strip()
    if not query:
        raise HTTPException(status_code=400, detail="메시지를 입력해주세요.")

    lower = query.lower()
    irrelevant_keywords = [
        "날씨", "주식", "코인", "비트코인", "로또", "요리", "레시피", "라면", "맛집",
        "파이썬 코드", "자바스크립트", "시 써줘", "노래 추천", "연예인", "대통령", "수학"
    ]
    for kw in irrelevant_keywords:
        if kw in lower:
            return {"reply": IRRELEVANT_RESPONSE, "is_guardrail": True}

    relevant_keywords = [
        "잔소리", "메이트", "zansori", "포트폴리오", "기획", "배경", "목적",
        "기능", "칸반", "회의록", "요약", "gemini", "기술", "스택", "개발", "팀장", "마감", "독촉"
    ]
    if not any(kw in lower for kw in relevant_keywords):
        return {"reply": IRRELEVANT_RESPONSE, "is_guardrail": True}

    if "스택" in lower or "기술" in lower:
        return {
            "reply": "잔소리메이트 백엔드는 FastAPI (Google Cloud Run 컨테이너) 및 Google Apps Script 기반으로 구축되어 있습니다.",
            "is_guardrail": False
        }

    return {
        "reply": "잔소리메이트는 AI가 회의록을 요약해 할 일을 쪼개주고, 맵고 달달한 페르소나 잔소리로 팀원들의 마감일을 챙겨주는 초간편 협업 플랫폼입니다.",
        "is_guardrail": False
    }

# 로컬 단독 실행 지원 (Cloud Run PORT 환경변수 준수)
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

