from sqlalchemy import Column, Integer, String, Date, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Patient(Base):
    __tablename__ = "patients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String(10))
    admission_date = Column(Date)
    care_grade = Column(String(20))  # 장기요양등급
    
    # 신체 기능
    mobility = Column(String(50))  # 독립/보조기/휠체어
    eating_ability = Column(String(50))  # 독립/부분도움/전적도움
    cognitive_function = Column(String(50))  # 정상/경도/중등도/중증
    swallowing_ability = Column(String(50))  # 정상/부드러운음식/유동식
    
    # 연락처
    guardian_id = Column(Integer, ForeignKey("users.id"))
    emergency_contact = Column(String)
    primary_doctor = Column(String)
    primary_hospital = Column(String)
    
    # Metadata
    notes = Column(Text)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    guardian = relationship("User", foreign_keys=[guardian_id])
    medical_conditions = relationship("MedicalCondition", back_populates="patient")
    medications = relationship("Medication", back_populates="patient")
    dietary_restrictions = relationship("DietaryRestriction", back_populates="patient")
    allergies = relationship("Allergy", back_populates="patient")
    meal_records = relationship("MealRecord", back_populates="patient")


class MedicalCondition(Base):
    __tablename__ = "medical_conditions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    condition_type = Column(String(100), nullable=False)  # 고혈압, 당뇨병 등
    diagnosed_date = Column(Date)
    severity = Column(String(20))  # 경증, 중증
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="medical_conditions")


class Medication(Base):
    __tablename__ = "medications"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    medication_name = Column(String(200), nullable=False)
    dosage = Column(String(100))
    frequency = Column(String(50))  # 1일 3회
    timing = Column(JSON)  # {"morning": true, "lunch": false, "dinner": true, "bedtime": false}
    start_date = Column(Date)
    end_date = Column(Date)
    notes = Column(Text)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="medications")


class DietaryRestriction(Base):
    __tablename__ = "dietary_restrictions"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    restriction_type = Column(String(50), nullable=False)  # 저염식, 당뇨식, 저단백식
    severity = Column(String(20))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="dietary_restrictions")


class Allergy(Base):
    __tablename__ = "allergies"
    
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    allergen = Column(String(100), nullable=False)
    reaction = Column(String(200))
    severity = Column(String(20))  # 경증, 중증, 아나필락시스
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    patient = relationship("Patient", back_populates="allergies")
