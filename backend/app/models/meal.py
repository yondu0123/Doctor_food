from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class MealRecord(Base):
    __tablename__ = "meal_records"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    caregiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    meal_type = Column(String(20), nullable=False)  # breakfast, lunch, dinner, snack
    photo_url = Column(String(500))
    
    # AI 분석 결과
    detected_foods = Column(JSON)  # [{"name": "현미밥", "amount": "1공기", "calories": 300}]
    portion_consumed = Column(String(20))  # full, half, quarter, none
    estimated_nutrition = Column(JSON)  # {"calories": 520, "protein": 25, "carbs": 70, "fat": 12, "sodium": 850}
    
    # 식이제한 준수 여부
    dietary_compliance = Column(JSON)  # {"status": "good", "issues": [], "notes": "저염식 기준 적합"}
    
    # 메타데이터
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    ai_confidence = Column(Float)  # 0.0 ~ 1.0
    manual_override = Column(Integer, default=0)  # 수동 수정 여부
    notes = Column(Text)
    
    # Relationships
    patient = relationship("Patient", back_populates="meal_records")
    caregiver = relationship("User", foreign_keys=[caregiver_id])


class NutritionDailySummary(Base):
    __tablename__ = "nutrition_daily_summary"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    # 영양소 합계
    total_calories = Column(Integer, default=0)
    total_protein = Column(Float, default=0.0)
    total_sodium = Column(Float, default=0.0)
    total_carbs = Column(Float, default=0.0)
    total_fat = Column(Float, default=0.0)
    
    # 통계
    meals_count = Column(Integer, default=0)
    photos_count = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    patient = relationship("Patient")


class DietPlan(Base):
    """AI 생성 식단 계획"""
    __tablename__ = "diet_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    date = Column(Date, nullable=False)
    
    # AI 생성 식단
    breakfast = Column(JSON)  # {"main": "현미밥", "soup": "된장국", "side_dishes": [...]}
    lunch = Column(JSON)
    dinner = Column(JSON)
    
    # 영양소 계획
    planned_nutrition = Column(JSON)  # {"calories": 1500, "protein": 60, ...}
    
    # 메타데이터
    generated_by = Column(String(50))  # gemini-1.5-flash
    ai_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient")
