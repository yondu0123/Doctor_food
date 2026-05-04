from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from .core.config import settings
from .core.database import engine, Base
from .api import meals

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI(
    title="닥터푸드 API",
    description="요양원 식사·투약·건강관리 통합 플랫폼",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 업로드 디렉토리 생성
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# 정적 파일 서빙 (업로드된 사진)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# API 라우터 등록
app.include_router(meals.router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "닥터푸드 API에 오신 것을 환영합니다!",
        "version": "1.0.0",
        "docs": "/docs",
        "features": [
            "식사 사진 AI 분석 (Gemini 1.5 Flash)",
            "영양소 자동 계산",
            "환자별 식이제한 준수 체크",
            "일일/주간/월간 영양 통계"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "environment": settings.ENVIRONMENT}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
