// 인증 헬퍼 함수
import { login, register, kakaoLogin, getCurrentUser, logout as apiLogout } from './api.js';

/**
 * 로그인 여부 확인
 * @returns {boolean}
 */
export function isAuthenticated() {
  return !!localStorage.getItem('access_token');
}

/**
 * 현재 사용자 정보 가져오기
 * @returns {Object|null}
 */
export function getCurrentUserInfo() {
  const userStr = localStorage.getItem('user');
  return userStr ? JSON.parse(userStr) : null;
}

/**
 * 사용자 정보 저장
 * @param {Object} user
 */
export function saveUserInfo(user) {
  localStorage.setItem('user', JSON.stringify(user));
}

/**
 * 인증 체크 (페이지 보호용)
 * @returns {boolean}
 */
export function checkAuth() {
  if (!isAuthenticated()) {
    const currentPath = window.location.pathname;
    localStorage.setItem('redirect_after_login', currentPath);
    window.location.href = '/pages/login.html';
    return false;
  }
  return true;
}

/**
 * 역할별 대시보드로 리다이렉트
 * @param {string} role - admin, caregiver, guardian
 */
export function redirectToDashboard(role) {
  const dashboardMap = {
    'admin': '/pages/admin/admin.html',
    'caregiver': '/pages/caregiver/caregiver.html',
    'guardian': '/pages/guardian/guardian.html'
  };
  
  const redirectPath = localStorage.getItem('redirect_after_login');
  localStorage.removeItem('redirect_after_login');
  
  window.location.href = redirectPath || dashboardMap[role] || '/';
}

/**
 * 이메일/비밀번호 로그인 처리
 * @param {string} email
 * @param {string} password
 * @returns {Promise}
 */
export async function handleLogin(email, password) {
  try {
    showLoading('로그인 중...');
    
    // 로그인 API 호출
    await login(email, password);
    
    // 사용자 정보 조회
    const user = await getCurrentUser();
    saveUserInfo(user);
    
    hideLoading();
    showSuccess('로그인 성공!');
    
    // 역할별 대시보드로 이동
    setTimeout(() => {
      redirectToDashboard(user.role);
    }, 500);
    
  } catch (error) {
    hideLoading();
    showError(error.message || '로그인에 실패했습니다');
    throw error;
  }
}

/**
 * 회원가입 처리
 * @param {Object} userData
 * @returns {Promise}
 */
export async function handleRegister(userData) {
  try {
    showLoading('회원가입 중...');
    
    // 회원가입 API 호출
    await register(userData);
    
    hideLoading();
    showSuccess('회원가입 성공! 로그인 페이지로 이동합니다.');
    
    // 로그인 페이지로 이동
    setTimeout(() => {
      window.location.href = '/pages/login.html';
    }, 1500);
    
  } catch (error) {
    hideLoading();
    showError(error.message || '회원가입에 실패했습니다');
    throw error;
  }
}

/**
 * 카카오 로그인 처리
 * @param {string} code - 카카오 인가 코드
 * @param {string} redirectUri - 리다이렉트 URI
 * @returns {Promise}
 */
export async function handleKakaoLogin(code, redirectUri) {
  try {
    showLoading('카카오 로그인 중...');
    
    // 카카오 로그인 API 호출
    await kakaoLogin(code, redirectUri);
    
    // 사용자 정보 조회
    const user = await getCurrentUser();
    saveUserInfo(user);
    
    hideLoading();
    showSuccess('로그인 성공!');
    
    // 역할별 대시보드로 이동
    setTimeout(() => {
      redirectToDashboard(user.role);
    }, 500);
    
  } catch (error) {
    hideLoading();
    showError(error.message || '카카오 로그인에 실패했습니다');
    throw error;
  }
}

/**
 * 로그아웃
 */
export function handleLogout() {
  apiLogout();
  window.location.href = '/';
}

/**
 * 에러 메시지 표시
 * @param {string} message
 */
export function showError(message) {
  const toast = createToast(message, 'error');
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('show');
  }, 10);
  
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/**
 * 성공 메시지 표시
 * @param {string} message
 */
export function showSuccess(message) {
  const toast = createToast(message, 'success');
  document.body.appendChild(toast);
  
  setTimeout(() => {
    toast.classList.add('show');
  }, 10);
  
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

/**
 * 로딩 표시
 * @param {string} message
 */
export function showLoading(message = '처리 중...') {
  let loader = document.getElementById('global-loader');
  if (!loader) {
    loader = document.createElement('div');
    loader.id = 'global-loader';
    loader.innerHTML = `
      <div class="loader-backdrop">
        <div class="loader-content">
          <div class="spinner"></div>
          <p class="loader-message">${message}</p>
        </div>
      </div>
    `;
    document.body.appendChild(loader);
  } else {
    loader.querySelector('.loader-message').textContent = message;
  }
  loader.style.display = 'flex';
}

/**
 * 로딩 숨기기
 */
export function hideLoading() {
  const loader = document.getElementById('global-loader');
  if (loader) {
    loader.style.display = 'none';
  }
}

/**
 * 토스트 생성
 * @param {string} message
 * @param {string} type - success, error
 * @returns {HTMLElement}
 */
function createToast(message, type) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === 'success' ? '✓' : '✕';
  const bgColor = type === 'success' ? '#22c55e' : '#ef4444';
  
  toast.innerHTML = `
    <div style="
      position: fixed;
      top: 24px;
      right: 24px;
      background: ${bgColor};
      color: white;
      padding: 16px 24px;
      border-radius: 12px;
      box-shadow: 0 10px 24px rgba(0,0,0,0.2);
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 600;
      z-index: 9999;
      opacity: 0;
      transform: translateY(-20px);
      transition: all 0.3s ease;
    ">
      <span style="font-size: 20px;">${icon}</span>
      <span>${message}</span>
    </div>
  `;
  
  return toast.firstElementChild;
}

// 전역 스타일 추가
const style = document.createElement('style');
style.textContent = `
  .toast.show {
    opacity: 1 !important;
    transform: translateY(0) !important;
  }
  
  #global-loader {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: none;
    align-items: center;
    justify-content: center;
    z-index: 10000;
  }
  
  .loader-content {
    background: white;
    padding: 32px;
    border-radius: 16px;
    text-align: center;
  }
  
  .spinner {
    width: 48px;
    height: 48px;
    border: 4px solid #e5e7eb;
    border-top-color: #22c55e;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin: 0 auto 16px;
  }
  
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  
  .loader-message {
    color: #1f2937;
    font-weight: 600;
    margin: 0;
  }
`;
document.head.appendChild(style);
