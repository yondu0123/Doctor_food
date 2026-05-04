from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import os
import uuid
from ..core.database import get_db
from ..core.config import settings
from ..models.user import User
from ..models.patient import Patient
from ..models.meal import MealRecord, NutritionDailySummary
from ..auth.dependencies import get_current_user
from ..services.gemini_meal_analyzer import get_meal_analyzer

router = APIRouter(prefix="/meals", tags=["meals"])


@router.post("/upload")
async def upload_meal_photo(
    patient_id: int = Form(...),
    meal_type: str = Form(...),  # breakfast, lunch, dinner, snack
    photo: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    식사 사진 업로드 및 AI 분석
    
    - 간병인이 환자의 식사 사진을 업로드
    - Gemini AI가 자동으로 음식 종류, 영양소, 섭취량 분석
    - 분석 결과를 DB에 저장
    """
    
    # 환자 존재 확인
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="환자를 찾을 수 없습니다")
    
    # 업로드 디렉토리 생성
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    # 파일 저장
    file_extension = os.path.splitext(photo.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, unique_filename)
    
    with open(file_path, "wb") as buffer:
        content = await photo.read()
        buffer.write(content)
    
    # 환자 정보 수집
    patient_info = {
        "age": (datetime.now().date() - patient.birth_date).days // 365,
        "conditions": [mc.condition_type for mc in patient.medical_conditions],
        "restrictions": [dr.restriction_type for dr in patient.dietary_restrictions],
        "allergies": [a.allergen for a in patient.allergies]
    }
    
    # Gemini AI 분석
    analyzer = get_meal_analyzer()
    analysis_result = await analyzer.analyze_meal_photo(file_path, patient_info)
    
    # DB에 저장
    meal_record = MealRecord(
        patient_id=patient_id,
        caregiver_id=current_user.id,
        meal_type=meal_type,
        photo_url=file_path,
        detected_foods=analysis_result["foods"],
        portion_consumed=analysis_result["portion_consumed"],
        estimated_nutrition=analysis_result["total_nutrition"],
        dietary_compliance=analysis_result["dietary_compliance"],
        ai_confidence=analysis_result["confidence"]
    )
    
    db.add(meal_record)
    db.commit()
    db.refresh(meal_record)
    
    # 일일 영양소 요약 업데이트
    await update_daily_nutrition_summary(db, patient_id, datetime.now().date())
    
    return {
        "success": True,
        "meal_record_id": meal_record.id,
        "analysis": analysis_result,
        "message": "식사 기록이 저장되었습니다"
    }


@router.get("/{patient_id}")
async def get_meal_history(
    patient_id: int,
    date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    환자의 식사 이력 조회
    
    - 특정 날짜 또는 최근 식사 기록 조회
    - 보호자/간병인/관리자 모두 접근 가능
    """
    
    query = db.query(MealRecord).filter(MealRecord.patient_id == patient_id)
    
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        query = query.filter(
            db.func.date(MealRecord.recorded_at) == target_date
        )
    
    meals = query.order_by(MealRecord.recorded_at.desc()).limit(20).all()
    
    # 일일 영양소 요약
    summary_date = datetime.strptime(date, "%Y-%m-%d").date() if date else datetime.now().date()
    daily_summary = db.query(NutritionDailySummary).filter(
        NutritionDailySummary.patient_id == patient_id,
        NutritionDailySummary.date == summary_date
    ).first()
    
    return {
        "meals": [
            {
                "id": meal.id,
                "meal_type": meal.meal_type,
                "photo_url": meal.photo_url,
                "detected_foods": meal.detected_foods,
                "portion_consumed": meal.portion_consumed,
                "estimated_nutrition": meal.estimated_nutrition,
                "dietary_compliance": meal.dietary_compliance,
                "recorded_at": meal.recorded_at,
                "ai_confidence": meal.ai_confidence
            }
            for meal in meals
        ],
        "daily_summary": {
            "total_calories": daily_summary.total_calories if daily_summary else 0,
            "total_protein": daily_summary.total_protein if daily_summary else 0,
            "total_sodium": daily_summary.total_sodium if daily_summary else 0,
            "meals_count": daily_summary.meals_count if daily_summary else 0
        } if daily_summary else None
    }


@router.get("/nutrition/summary/{patient_id}")
async def get_nutrition_summary(
    patient_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    환자의 영양소 통계 조회
    
    - 기간별 영양소 섭취 추이
    - 평균 칼로리, 단백질, 나트륨 등
    """
    
    query = db.query(NutritionDailySummary).filter(
        NutritionDailySummary.patient_id == patient_id
    )
    
    if start_date:
        query = query.filter(NutritionDailySummary.date >= datetime.strptime(start_date, "%Y-%m-%d").date())
    if end_date:
        query = query.filter(NutritionDailySummary.date <= datetime.strptime(end_date, "%Y-%m-%d").date())
    
    summaries = query.order_by(NutritionDailySummary.date).all()
    
    if not summaries:
        return {"message": "데이터가 없습니다", "summaries": []}
    
    # 평균 계산
    avg_calories = sum(s.total_calories for s in summaries) / len(summaries)
    avg_protein = sum(s.total_protein for s in summaries) / len(summaries)
    avg_sodium = sum(s.total_sodium for s in summaries) / len(summaries)
    
    return {
        "period": {
            "start": summaries[0].date,
            "end": summaries[-1].date,
            "days": len(summaries)
        },
        "averages": {
            "calories": round(avg_calories, 1),
            "protein": round(avg_protein, 1),
            "sodium": round(avg_sodium, 1)
        },
        "daily_data": [
            {
                "date": s.date,
                "calories": s.total_calories,
                "protein": s.total_protein,
                "sodium": s.total_sodium,
                "meals_count": s.meals_count
            }
            for s in summaries
        ]
    }


async def update_daily_nutrition_summary(db: Session, patient_id: int, target_date: date):
    """일일 영양소 요약 업데이트"""
    
    # 해당 날짜의 모든 식사 기록 조회
    meals = db.query(MealRecord).filter(
        MealRecord.patient_id == patient_id,
        db.func.date(MealRecord.recorded_at) == target_date
    ).all()
    
    # 영양소 합계 계산
    total_calories = sum(meal.estimated_nutrition.get("calories", 0) for meal in meals)
    total_protein = sum(meal.estimated_nutrition.get("protein", 0) for meal in meals)
    total_sodium = sum(meal.estimated_nutrition.get("sodium", 0) for meal in meals)
    total_carbs = sum(meal.estimated_nutrition.get("carbs", 0) for meal in meals)
    total_fat = sum(meal.estimated_nutrition.get("fat", 0) for meal in meals)
    
    # 기존 요약 조회 또는 생성
    summary = db.query(NutritionDailySummary).filter(
        NutritionDailySummary.patient_id == patient_id,
        NutritionDailySummary.date == target_date
    ).first()
    
    if summary:
        # 업데이트
        summary.total_calories = total_calories
        summary.total_protein = total_protein
        summary.total_sodium = total_sodium
        summary.total_carbs = total_carbs
        summary.total_fat = total_fat
        summary.meals_count = len(meals)
        summary.photos_count = sum(1 for meal in meals if meal.photo_url)
    else:
        # 새로 생성
        summary = NutritionDailySummary(
            patient_id=patient_id,
            date=target_date,
            total_calories=total_calories,
            total_protein=total_protein,
            total_sodium=total_sodium,
            total_carbs=total_carbs,
            total_fat=total_fat,
            meals_count=len(meals),
            photos_count=sum(1 for meal in meals if meal.photo_url)
        )
        db.add(summary)
    
    db.commit()
