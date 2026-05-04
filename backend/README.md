# 닥터푸드 백엔드 API

요양원 식사·투약·건강관리 통합 플랫폼 백엔드

## 🚀 주요 기능

### ✅ 구현 완료
- **식사 사진 AI 분석** (Gemini 1.5 Flash)
  - 음식 종류 자동 인식
  - 영양소 자동 계산 (칼로리, 단백질, 나트륨 등)
  - 섭취량 추정 (완식/반/1/3)
  - 식이제한 준수 여부 체크
- **영양소 통계**
  - 일일/주간/월간 영양 통계
  - 환자별 영양소 추이 분석
- **데이터베이스 설계**
  - 환자 정보 (기저질환, 식이제한, 알레르기)
  - 식사 기록 (사진 + AI 분석 결과)
  - 영양소 일일 요약

### 🔜 개발 예정
- 사용자 인증 (JWT)
- 환자 등록 API
- 투약 관리 API
- AI 식단 추천
- 보호자 알림 시스템

---

## 📦 설치 방법

### 1. 가상환경 생성 및 활성화
```bash
cd backend
python -m venv venv

# macOS/Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정
```bash
cp .env.example .env
```

`.env` 파일을 열어서 다음 값을 설정:
```env
# Google Gemini API 키 (필수!)
GOOGLE_API_KEY=your-gemini-api-key-here

# JWT 시크릿 키 (프로덕션에서는 반드시 변경)
SECRET_KEY=your-secret-key-here
```

**Gemini API 키 발급 방법:**
1. https://makersuite.google.com/app/apikey 접속
2. "Create API Key" 클릭
3. 생성된 키를 `.env` 파일에 붙여넣기

---

## 🏃 실행 방법

### 개발 서버 실행
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면:
- API 문서: http://localhost:8000/docs
- 메인 페이지: http://localhost:8000

---

## 📡 API 엔드포인트

### 식사 관리

#### 1. 식사 사진 업로드 및 AI 분석
```http
POST /api/meals/upload
Content-Type: multipart/form-data

Parameters:
- patient_id: int (환자 ID)
- meal_type: string (breakfast/lunch/dinner/snack)
- photo: file (사진 파일)

Response:
{
  "success": true,
  "meal_record_id": 1,
  "analysis": {
    "foods": [
      {"name": "현미밥", "amount": "1공기", "calories": 300},
      {"name": "된장국", "amount": "1그릇", "calories": 50}
    ],
    "total_nutrition": {
      "calories": 520,
      "protein": 25.5,
      "carbs": 70.2,
      "fat": 12.3,
      "sodium": 850
    },
    "portion_consumed": "full",
    "dietary_compliance": {
      "status": "good",
      "issues": [],
      "notes": "저염식 기준 적합"
    },
    "confidence": 0.85
  }
}
```

#### 2. 식사 이력 조회
```http
GET /api/meals/{patient_id}?date=2026-05-04

Response:
{
  "meals": [...],
  "daily_summary": {
    "total_calories": 1520,
    "total_protein": 65.5,
    "total_sodium": 2100,
    "meals_count": 3
  }
}
```

#### 3. 영양소 통계 조회
```http
GET /api/meals/nutrition/summary/{patient_id}?start_date=2026-05-01&end_date=2026-05-07

Response:
{
  "period": {"start": "2026-05-01", "end": "2026-05-07", "days": 7},
  "averages": {
    "calories": 1550.5,
    "protein": 62.3,
    "sodium": 2050.0
  },
  "daily_data": [...]
}
```

---

## 🗄️ 데이터베이스 구조

### 주요 테이블
- `users` - 사용자 (관리자/간병인/보호자)
- `patients` - 환자 정보
- `medical_conditions` - 기저질환
- `medications` - 복용 약물
- `dietary_restrictions` - 식이제한
- `allergies` - 알레르기
- `meal_records` - 식사 기록 (사진 + AI 분석)
- `nutrition_daily_summary` - 일일 영양소 요약
- `diet_plans` - AI 생성 식단 계획

---

## 🤖 Gemini AI 분석 프로세스

1. **사진 업로드** → 서버에 저장
2. **환자 정보 수집** → 기저질환, 식이제한, 알레르기
3. **Gemini 분석 요청** → 음식 인식 + 영양소 계산
4. **결과 검증** → JSON 파싱 + 필수 필드 확인
5. **DB 저장** → 식사 기록 + 영양소 요약 업데이트
6. **응답 반환** → 프론트엔드로 분석 결과 전송

---

## 🧪 테스트 방법

### 1. API 문서에서 직접 테스트
http://localhost:8000/docs 접속 후 "Try it out" 버튼 클릭

### 2. curl로 테스트
```bash
# 식사 사진 업로드
curl -X POST "http://localhost:8000/api/meals/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "patient_id=1" \
  -F "meal_type=lunch" \
  -F "photo=@/path/to/meal_photo.jpg"
```

---

## 📝 다음 단계

### Phase 1 (완료)
- [x] 프로젝트 구조 설정
- [x] 데이터베이스 모델 설계
- [x] Gemini 식사 분석 서비스
- [x] 식사 업로드 API
- [x] 영양소 통계 API

### Phase 2 (진행 중)
- [ ] 사용자 인증 API (회원가입/로그인)
- [ ] 환자 등록 API (다단계 폼)
- [ ] 투약 관리 API
- [ ] AI 식단 추천 API

### Phase 3 (예정)
- [ ] 보호자 알림 시스템
- [ ] 프론트엔드 연동
- [ ] 파일럿 테스트

---

## 💡 개발 팁

### Gemini API 무료 한도
- **일일 1,500회** 무료
- 초과 시 유료 전환 필요
- 비용: $0.00025/1K tokens (매우 저렴!)

### 데이터베이스
- 개발: SQLite (파일 기반, 간단)
- 프로덕션: PostgreSQL 권장

### 보안
- `.env` 파일은 절대 Git에 커밋하지 말 것
- 프로덕션에서는 SECRET_KEY 반드시 변경
- HTTPS 사용 권장

---

## 🐛 문제 해결

### Gemini API 오류
```
ValueError: GOOGLE_API_KEY가 설정되지 않았습니다.
```
→ `.env` 파일에 `GOOGLE_API_KEY` 설정 확인

### 데이터베이스 오류
```
sqlalchemy.exc.OperationalError: no such table
```
→ 서버 재시작 (테이블 자동 생성됨)

### CORS 오류
→ `app/core/config.py`에서 `ALLOWED_ORIGINS` 확인

---

## 📞 문의

문제가 있거나 질문이 있으면 이슈를 등록해주세요!
