# 닥터푸드 (DoctorFood)

> 요양원 식사·투약·건강관리 통합 플랫폼

AI 기반 식사 분석과 영양소 자동 계산으로 요양 현장의 케어 품질을 높이는 서비스입니다.

## 🎯 핵심 기능

### ✅ 구현 완료
- **식사 사진 AI 분석** (Gemini 1.5 Flash 무료!)
  - 음식 종류 자동 인식
  - 영양소 자동 계산 (칼로리, 단백질, 나트륨 등)
  - 섭취량 추정 (완식/반/1/3)
  - 환자별 식이제한 준수 체크
- **영양소 통계**
  - 일일/주간/월간 영양 통계
  - 환자별 영양소 추이 분석
- **3자 앱 구조**
  - 관리자 대시보드
  - 간병인 앱
  - 보호자 앱

### 🔜 개발 예정
- 사용자 인증 (JWT)
- 환자 등록 API
- 투약 관리
- AI 식단 추천
- 보호자 실시간 알림

---

## 📁 프로젝트 구조

```
doctorfood-app/
├── frontend/              # 프론트엔드
│   ├── index.html        # 랜딩 페이지
│   ├── pages/
│   │   ├── admin/        # 관리자 대시보드
│   │   ├── caregiver/    # 간병인 앱
│   │   └── guardian/     # 보호자 앱
│   ├── shared/
│   │   ├── js/
│   │   │   ├── api.js    # API 통신
│   │   │   └── app.js    # 공통 로직
│   │   └── css/
│   └── README.md
│
├── backend/              # 백엔드 (FastAPI)
│   ├── app/
│   │   ├── api/         # API 엔드포인트
│   │   ├── models/      # DB 모델
│   │   ├── services/    # Gemini AI
│   │   └── main.py
│   ├── requirements.txt
│   └── README.md
│
└── README.md            # 이 파일
```

---

## 🚀 빠른 시작

### 1. 백엔드 실행
```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일에서 GOOGLE_API_KEY 설정 필수!

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

**Gemini API 키 발급:**
1. https://makersuite.google.com/app/apikey
2. "Create API Key" 클릭
3. `.env` 파일에 붙여넣기

### 2. 프론트엔드 실행
```bash
cd frontend

# 간단한 HTTP 서버
python -m http.server 3000

# 또는 VS Code Live Server 사용
```

### 3. 접속
- 백엔드 API: http://localhost:8000/docs
- 프론트엔드: http://localhost:3000

---

## 📡 API 예시

### 식사 사진 업로드 및 AI 분석
```bash
curl -X POST "http://localhost:8000/api/meals/upload" \
  -F "patient_id=1" \
  -F "meal_type=lunch" \
  -F "photo=@meal.jpg"
```

**응답:**
```json
{
  "success": true,
  "analysis": {
    "foods": [
      {"name": "현미밥", "amount": "1공기", "calories": 300},
      {"name": "된장국", "amount": "1그릇", "calories": 50}
    ],
    "total_nutrition": {
      "calories": 520,
      "protein": 25.5,
      "sodium": 850
    },
    "portion_consumed": "full",
    "confidence": 0.85
  }
}
```

---

## 🎨 화면 구성

### 관리자 대시보드
- 전체 환자 통계
- 영양소 추이 차트
- 누락 모니터링
- AI 식단 추천

### 간병인 앱
- 식사 사진 촬영 & 업로드
- AI 분석 결과 즉시 확인
- 투약 체크리스트
- 환자 상태 기록

### 보호자 앱
- 실시간 식사 사진 확인
- 영양소 통계 조회
- 일일 케어 리포트
- 메시지 전송

---

## 🤖 기술 스택

### 백엔드
- **FastAPI** - 고성능 Python 웹 프레임워크
- **SQLAlchemy** - ORM
- **SQLite** - 개발용 DB (프로덕션: PostgreSQL)
- **Google Gemini 1.5 Flash** - AI 식사 분석 (무료!)
- **JWT** - 인증

### 프론트엔드
- **HTML5 / CSS3** - 구조 & 스타일
- **Vanilla JavaScript** - 로직
- **Fetch API** - 백엔드 통신

---

## 💡 차별화 포인트

1. **Gemini AI 무료 활용**
   - 일일 1,500회 무료
   - GPT-4 대비 비용 0원!

2. **식사 사진 → 영양소 자동 계산**
   - 수기 입력 불필요
   - 간병인 업무 부담 ↓

3. **3자 통합 플랫폼**
   - 관리자 + 간병인 + 보호자
   - 데이터 흐름 일원화

4. **확장 가능한 구조**
   - 투약 관리
   - AI 식단 추천
   - 이상징후 감지

---

## 📝 개발 로드맵

### Phase 1 (완료) ✅
- [x] 프로젝트 구조 설정
- [x] 데이터베이스 모델 설계
- [x] Gemini 식사 분석 서비스
- [x] 식사 업로드 API
- [x] 영양소 통계 API
- [x] 프론트엔드 구조 정리

### Phase 2 (진행 중) 🚧
- [ ] 사용자 인증 API
- [ ] 환자 등록 API
- [ ] 투약 관리 API
- [ ] 프론트엔드 ↔ 백엔드 연결

### Phase 3 (예정) 📅
- [ ] AI 식단 추천
- [ ] 보호자 알림 시스템
- [ ] 파일럿 테스트
- [ ] 프로덕션 배포

---

## 🧪 테스트

### 백엔드 API 테스트
http://localhost:8000/docs 접속 후 "Try it out"

### 프론트엔드 테스트
1. 백엔드 실행 확인
2. 프론트엔드 접속
3. 간병인 앱에서 사진 업로드 테스트

---

## 📞 문의 & 기여

- 이슈: GitHub Issues
- 문의: 프로젝트 담당자

---

## 📄 라이선스

MIT License

---

## 🙏 감사

- Google Gemini API
- FastAPI
- 모든 기여자분들
