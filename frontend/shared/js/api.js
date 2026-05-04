// API 통신 중앙 관리
const API_BASE_URL = 'http://localhost:8000/api';

// 토큰 관리
function getToken() {
  return localStorage.getItem('access_token');
}

function setToken(token) {
  localStorage.setItem('access_token', token);
}

function removeToken() {
  localStorage.removeItem('access_token');
}

// API 호출 헬퍼
async function apiCall(endpoint, options = {}) {
  const token = getToken();
  const headers = {
    ...options.headers,
  };
  
  if (token && !options.skipAuth) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  // FormData가 아닌 경우에만 Content-Type 설정
  if (!(options.body instanceof FormData) && options.body) {
    headers['Content-Type'] = 'application/json';
  }
  
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: '서버 오류' }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('API 오류:', error);
    throw error;
  }
}

// ===== 식사 관리 API =====

/**
 * 식사 사진 업로드 및 AI 분석
 * @param {number} patientId - 환자 ID
 * @param {string} mealType - 식사 유형 (breakfast/lunch/dinner/snack)
 * @param {File} photoFile - 사진 파일
 * @returns {Promise} 분석 결과
 */
export async function uploadMealPhoto(patientId, mealType, photoFile) {
  const formData = new FormData();
  formData.append('patient_id', patientId);
  formData.append('meal_type', mealType);
  formData.append('photo', photoFile);
  
  return await apiCall('/meals/upload', {
    method: 'POST',
    body: formData
  });
}

/**
 * 환자의 식사 이력 조회
 * @param {number} patientId - 환자 ID
 * @param {string} date - 날짜 (YYYY-MM-DD, 선택)
 * @returns {Promise} 식사 이력
 */
export async function getMealHistory(patientId, date = null) {
  const params = date ? `?date=${date}` : '';
  return await apiCall(`/meals/${patientId}${params}`);
}

/**
 * 영양소 통계 조회
 * @param {number} patientId - 환자 ID
 * @param {string} startDate - 시작 날짜 (YYYY-MM-DD, 선택)
 * @param {string} endDate - 종료 날짜 (YYYY-MM-DD, 선택)
 * @returns {Promise} 영양소 통계
 */
export async function getNutritionSummary(patientId, startDate = null, endDate = null) {
  const params = new URLSearchParams();
  if (startDate) params.append('start_date', startDate);
  if (endDate) params.append('end_date', endDate);
  
  const queryString = params.toString();
  return await apiCall(`/meals/nutrition/summary/${patientId}${queryString ? '?' + queryString : ''}`);
}

// ===== 인증 API (추후 구현) =====

/**
 * 로그인
 * @param {string} username - 사용자명
 * @param {string} password - 비밀번호
 * @returns {Promise} 토큰 정보
 */
export async function login(username, password) {
  const formData = new FormData();
  formData.append('username', username);
  formData.append('password', password);
  
  const result = await apiCall('/auth/login', {
    method: 'POST',
    body: formData,
    skipAuth: true
  });
  
  setToken(result.access_token);
  return result;
}

/**
 * 로그아웃
 */
export function logout() {
  removeToken();
  window.location.href = '/';
}

/**
 * 현재 사용자 정보 조회
 * @returns {Promise} 사용자 정보
 */
export async function getCurrentUser() {
  return await apiCall('/auth/me');
}

// ===== 환자 관리 API (추후 구현) =====

/**
 * 환자 목록 조회
 * @returns {Promise} 환자 목록
 */
export async function getPatients() {
  return await apiCall('/patients');
}

/**
 * 환자 상세 정보 조회
 * @param {number} patientId - 환자 ID
 * @returns {Promise} 환자 정보
 */
export async function getPatient(patientId) {
  return await apiCall(`/patients/${patientId}`);
}

/**
 * 환자 등록
 * @param {Object} patientData - 환자 정보
 * @returns {Promise} 등록된 환자 정보
 */
export async function createPatient(patientData) {
  return await apiCall('/patients', {
    method: 'POST',
    body: JSON.stringify(patientData)
  });
}

// ===== 유틸리티 =====

/**
 * 로그인 여부 확인
 * @returns {boolean}
 */
export function isAuthenticated() {
  return !!getToken();
}

/**
 * 날짜 포맷팅 (YYYY-MM-DD)
 * @param {Date} date
 * @returns {string}
 */
export function formatDate(date) {
  return date.toISOString().split('T')[0];
}

/**
 * 오늘 날짜 가져오기
 * @returns {string} YYYY-MM-DD
 */
export function getToday() {
  return formatDate(new Date());
}
