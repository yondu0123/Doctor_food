# 📡 API 문서

> DoctorFood 백엔드 REST API 엔드포인트

---

## 🔐 인증 (Authentication)

### 1. 이메일 회원가입
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "홍길동",
  "phone": "010-1234-5678",
  "role": "caregiver"
}
```

**Response (201)**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user",
  "full_name": "홍길동",
  "role": "caregiver",
  "oauth_provider": "email"
}
```

---

### 2. 이메일 로그인
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "user",
    "full_name": "홍길동",
    "role": "caregiver"
  }
}
```

---

### 3. 카카오 OAuth 로그인
```http
POST /api/auth/kakao/login
Content-Type: application/json

{
  "code": "authorization_code_from_kakao",
  "role": "caregiver"
}
```

**Response (200)**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 2,
    "email": "kakao_user@kakao.com",
    "username": "kakao_user",
    "full_name": "김카카오",
    "role": "caregiver",
    "oauth_provider": "kakao",
    "profile_image": "https://..."
  }
}
```

---

### 4. 현재 사용자 정보
```http
GET /api/auth/me
Authorization: Bearer {access_token}
```

**Response (200)**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "user",
  "full_name": "홍길동",
  "role": "caregiver",
  "oauth_provider": "email",
  "created_at": "2026-05-04T10:00:00Z"
}
```

---

## 🍽️ 식사 관리 (Meals)

### 1. 식사 사진 분석 및 등록
```http
POST /api/meals/
Authorization: Bearer {access_token}
Content-Type: multipart/form-data

patient_id: 1
meal_type: "breakfast"
meal_date: "2026-05-04"
image: [파일]
notes: "아침 식사 완식"
```

**Response (200)**
```json
{
  "id": 1,
  "patient_id": 1,
  "meal_type": "breakfast",
  "meal_date": "2026-05-04",
  "image_url": "/uploads/meals/20260504_123456.jpg",
  "ai_analysis": {
    "foods": ["밥", "된장찌개", "김치", "계란후라이"],
    "calories": 520,
    "protein": 25.5,
    "carbs": 68.0,
    "fat": 12.3,
    "sodium": 890,
    "portion_consumed": "완식",
    "dietary_compliance": true,
    "warnings": []
  },
  "notes": "아침 식사 완식",
  "created_at": "2026-05-04T08:30:00Z"
}
```

---

### 2. 식사 기록 조회
```http
GET /api/meals/?patient_id=1&start_date=2026-05-01&end_date=2026-05-07
Authorization: Bearer {access_token}
```

**Response (200)**
```json
[
  {
    "id": 1,
    "patient_id": 1,
    "meal_type": "breakfast",
    "meal_date": "2026-05-04",
    "image_url": "/uploads/meals/20260504_123456.jpg",
    "ai_analysis": { ... },
    "created_at": "2026-05-04T08:30:00Z"
  },
  ...
]
```

---

### 3. 영양소 통계
```http
GET /api/meals/nutrition-stats?patient_id=1&period=week
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `patient_id`: 환자 ID (필수)
- `period`: `day` | `week` | `month` (기본값: week)
- `start_date`: 시작일 (선택)
- `end_date`: 종료일 (선택)

**Response (200)**
```json
{
  "period": "week",
  "start_date": "2026-04-28",
  "end_date": "2026-05-04",
  "daily_stats": [
    {
      "date": "2026-05-04",
      "total_calories": 1850,
      "total_protein": 75.5,
      "total_carbs": 245.0,
      "total_fat": 52.3,
      "total_sodium": 2450,
      "meal_count": 3
    },
    ...
  ],
  "average": {
    "calories": 1820,
    "protein": 72.3,
    "carbs": 238.5,
    "fat": 50.1,
    "sodium": 2380
  }
}
```

---

## 👤 환자 관리 (Patients)

### 1. 환자 등록
```http
POST /api/patients/
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "김환자",
  "birth_date": "1950-03-15",
  "gender": "male",
  "room_number": "201",
  "medical_conditions": ["당뇨", "고혈압"],
  "dietary_restrictions": ["저염식", "당뇨식"],
  "allergies": ["땅콩", "새우"],
  "guardian_name": "김보호",
  "guardian_phone": "010-9876-5432"
}
```

**Response (201)**
```json
{
  "id": 1,
  "name": "김환자",
  "birth_date": "1950-03-15",
  "age": 76,
  "gender": "male",
  "room_number": "201",
  "medical_conditions": ["당뇨", "고혈압"],
  "dietary_restrictions": ["저염식", "당뇨식"],
  "allergies": ["땅콩", "새우"],
  "guardian_name": "김보호",
  "guardian_phone": "010-9876-5432",
  "is_active": true,
  "created_at": "2026-05-04T10:00:00Z"
}
```

---

### 2. 환자 목록 조회
```http
GET /api/patients/?is_active=true
Authorization: Bearer {access_token}
```

**Response (200)**
```json
[
  {
    "id": 1,
    "name": "김환자",
    "age": 76,
    "gender": "male",
    "room_number": "201",
    "medical_conditions": ["당뇨", "고혈압"],
    "is_active": true
  },
  ...
]
```

---

### 3. 환자 상세 조회
```http
GET /api/patients/1
Authorization: Bearer {access_token}
```

**Response (200)**
```json
{
  "id": 1,
  "name": "김환자",
  "birth_date": "1950-03-15",
  "age": 76,
  "gender": "male",
  "room_number": "201",
  "medical_conditions": ["당뇨", "고혈압"],
  "dietary_restrictions": ["저염식", "당뇨식"],
  "allergies": ["땅콩", "새우"],
  "guardian_name": "김보호",
  "guardian_phone": "010-9876-5432",
  "is_active": true,
  "created_at": "2026-05-04T10:00:00Z",
  "updated_at": "2026-05-04T10:00:00Z"
}
```

---

### 4. 환자 정보 수정
```http
PUT /api/patients/1
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "room_number": "202",
  "guardian_phone": "010-1111-2222"
}
```

**Response (200)**
```json
{
  "id": 1,
  "name": "김환자",
  "room_number": "202",
  "guardian_phone": "010-1111-2222",
  ...
}
```

---

## 🔒 인증 헤더

모든 보호된 엔드포인트는 JWT 토큰이 필요합니다:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## ⚠️ 에러 응답

### 400 Bad Request
```json
{
  "detail": "이미 등록된 이메일입니다"
}
```

### 401 Unauthorized
```json
{
  "detail": "인증되지 않은 사용자입니다"
}
```

### 403 Forbidden
```json
{
  "detail": "권한이 없습니다"
}
```

### 404 Not Found
```json
{
  "detail": "환자를 찾을 수 없습니다"
}
```

### 500 Internal Server Error
```json
{
  "detail": "서버 오류가 발생했습니다"
}
```

---

## 📊 응답 코드

| 코드 | 설명 |
|------|------|
| 200 | 성공 |
| 201 | 생성 성공 |
| 400 | 잘못된 요청 |
| 401 | 인증 실패 |
| 403 | 권한 없음 |
| 404 | 리소스 없음 |
| 500 | 서버 오류 |

---

## 🔗 Base URL

- **개발**: `http://localhost:8000/api`
- **프로덕션**: `https://api.doctorfood.com/api`

---

**마지막 업데이트**: 2026년 5월 4일
