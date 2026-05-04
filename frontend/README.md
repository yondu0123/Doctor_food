# 닥터푸드 프론트엔드

요양원 식사·투약·건강관리 통합 플랫폼 프론트엔드

## 📁 프로젝트 구조

```
frontend/
├── index.html                    # 랜딩 페이지
├── pages/
│   ├── admin/
│   │   └── admin.html           # 관리자 대시보드
│   ├── caregiver/
│   │   └── caregiver.html       # 간병인 앱
│   └── guardian/
│       └── guardian.html        # 보호자 앱
├── shared/
│   ├── js/
│   │   ├── api.js               # API 통신 중앙 관리
│   │   └── app.js               # 공통 로직
│   └── css/
│       └── styles.css           # 공통 스타일
└── assets/
    └── images/                  # 이미지 파일
```

## 🚀 실행 방법

### 1. 간단한 HTTP 서버 실행
```bash
cd frontend
python -m http.server 3000
```

### 2. VS Code Live Server 사용
1. VS Code에서 `index.html` 열기
2. 우클릭 → "Open with Live Server"

### 3. 접속
- 랜딩 페이지: http://localhost:3000
- 관리자: http://localhost:3000/pages/admin/admin.html
- 간병인: http://localhost:3000/pages/caregiver/caregiver.html
- 보호자: http://localhost:3000/pages/guardian/guardian.html

## 🔗 백엔드 연결

### API 설정
`shared/js/api.js`에서 API 주소 설정:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

### 백엔드 실행 필요
프론트엔드만으로는 동작하지 않습니다. 백엔드 서버를 먼저 실행하세요:
```bash
cd ../backend
uvicorn app.main:app --reload --port 8000
```

## 📱 주요 기능

### 간병인 앱 (caregiver.html)
- 식사 사진 업로드
- AI 자동 분석 결과 확인
- 투약 기록
- 환자 상태 기록

### 보호자 앱 (guardian.html)
- 실시간 식사 사진 확인
- 영양소 통계 조회
- 일일 케어 리포트
- 메시지 전송

### 관리자 대시보드 (admin.html)
- 전체 환자 통계
- 영양소 추이 분석
- 누락 모니터링
- AI 식단 추천

## 🛠️ 개발 가이드

### API 호출 예시
```javascript
import { uploadMealPhoto, getMealHistory } from '../shared/js/api.js';

// 식사 사진 업로드
const result = await uploadMealPhoto(patientId, 'lunch', photoFile);
console.log(result.analysis);

// 식사 이력 조회
const history = await getMealHistory(patientId, '2026-05-04');
console.log(history.meals);
```

### 에러 처리
```javascript
try {
  const result = await uploadMealPhoto(1, 'lunch', file);
  showToast('✅ 업로드 성공!', 'success');
} catch (error) {
  showToast(`❌ 오류: ${error.message}`, 'error');
}
```

## 📝 TODO

- [ ] 로그인 페이지 추가
- [ ] 환자 등록 폼 연결
- [ ] 실시간 알림 기능
- [ ] 차트 라이브러리 통합 (Chart.js)
- [ ] 반응형 디자인 개선
- [ ] PWA 지원 (모바일 앱처럼)

## 🎨 디자인 시스템

### 색상
- Primary: `#22c55e` (녹색)
- Secondary: `#14532d` (진한 녹색)
- Background: `#f5f8f7`
- Text: `#1f2937`

### 폰트
- Noto Sans KR (Google Fonts)

## 🔧 기술 스택

- **HTML5** - 구조
- **CSS3** - 스타일
- **Vanilla JavaScript** - 로직
- **Fetch API** - 백엔드 통신
- **LocalStorage** - 토큰 저장

## 📞 문의

문제가 있으면 이슈를 등록해주세요!
