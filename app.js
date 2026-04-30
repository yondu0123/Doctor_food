// ===== 페이지 전환 =====
const pageNames = {
  'dashboard': '대시보드',
  'patients': '환자 관리',
  'ai-diet': 'AI 식단 추천',
  'medication': '투약 관리',
  'guardian': '보호자 알림',
  'ingredients': '식자재 관리'
};

function showPage(pageId) {
  // 모든 페이지 숨기기
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  // 선택한 페이지 보이기
  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');

  // 사이드바 활성화
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    if (item.getAttribute('onclick') && item.getAttribute('onclick').includes(pageId)) {
      item.classList.add('active');
    }
  });

  // 페이지 제목 업데이트
  document.getElementById('page-title').textContent = pageNames[pageId] || pageId;
}

// ===== 날짜 표시 =====
function updateDate() {
  const now = new Date();
  const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
  document.getElementById('page-date').textContent = now.toLocaleDateString('ko-KR', options);
}

// ===== AI 식단 생성 =====
function generateAIDiet() {
  const modal = document.getElementById('ai-modal');
  modal.classList.remove('hidden');

  const steps = ['step1', 'step2', 'step3', 'step4', 'step5'];
  const stepTexts = [
    '✅ 환자 건강 데이터 분석',
    '✅ 기저질환별 영양 요구량 계산',
    '✅ 공통 식자재 최적화',
    '✅ 개별 맞춤 식단 생성',
    '✅ 비용 최적화 완료'
  ];

  let currentStep = 0;

  const interval = setInterval(() => {
    if (currentStep < steps.length) {
      const stepEl = document.getElementById(steps[currentStep]);
      if (stepEl) {
        stepEl.textContent = stepTexts[currentStep];
        stepEl.classList.add('active', 'done');
      }
      currentStep++;
    } else {
      clearInterval(interval);
      setTimeout(() => {
        modal.classList.add('hidden');
        showToast('✅ AI 식단 생성 완료! 32명의 맞춤 식단이 생성되었습니다.', 'success');
        // 스텝 초기화
        steps.forEach((id, i) => {
          const el = document.getElementById(id);
          if (el) {
            el.classList.remove('active', 'done');
            el.textContent = ['✅ 환자 건강 데이터 분석', '⏳ 기저질환별 영양 요구량 계산', '⏳ 공통 식자재 최적화', '⏳ 개별 맞춤 식단 생성', '⏳ 비용 최적화 완료'][i];
          }
        });
        document.getElementById('step1').classList.add('active');
      }, 500);
    }
  }, 700);
}

// ===== 주차 변경 =====
let currentWeek = 0;
function changeWeek(dir) {
  currentWeek += dir;
  const now = new Date();
  now.setDate(now.getDate() + currentWeek * 7);
  const year = now.getFullYear();
  const month = now.getMonth() + 1;
  const weekNum = Math.ceil(now.getDate() / 7);
  document.getElementById('week-label').textContent = `${year}년 ${month}월 ${weekNum}주차`;
}

// ===== 알림 =====
function showNotification() {
  showToast('📋 새 알림: 김순자 어르신 혈압약 미복용, 보호자 메시지 2건', 'info');
}

// ===== 투약 완료 처리 =====
function markMedDone(name, time) {
  showToast(`✅ ${name} 어르신 ${time} 투약 완료로 기록되었습니다.`, 'success');
  // 버튼 비활성화
  const buttons = document.querySelectorAll('.btn-sm-red');
  buttons.forEach(btn => {
    if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(name)) {
      btn.closest('.med-patient-card').classList.remove('missed');
      btn.closest('.med-patient-card').classList.add('done');
      btn.closest('.med-patient-card').querySelector('.med-status').textContent = '✅ 완료';
      btn.closest('.med-patient-card').querySelector('.med-status').className = 'med-status done';
      btn.remove();
    }
  });
}

// ===== 환자 필터 =====
function filterPatients(type) {
  document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
  showToast(`${type === 'all' ? '전체' : type} 환자 필터 적용됨`, 'info');
}

// ===== 환자 상세 =====
function showPatientDetail(name) {
  showToast(`${name} 어르신 상세 정보 (상세 페이지 준비 중)`, 'info');
}

// ===== 환자 추가 =====
function openAddPatient() {
  showToast('환자 추가 폼 (개발 예정)', 'info');
}

// ===== 답장 전송 =====
function sendReply() {
  const inputs = document.querySelectorAll('.reply-input');
  inputs.forEach(input => {
    if (input.value.trim()) {
      showToast(`✅ 답장 전송 완료: "${input.value}"`, 'success');
      input.value = '';
    }
  });
}

// ===== 일일 리포트 전송 =====
function sendDailyReport() {
  showToast('📱 전체 보호자에게 오늘의 케어 리포트가 발송되었습니다!', 'success');
}

// ===== 토스트 메시지 =====
function showToast(message, type = '') {
  const toast = document.getElementById('toast');
  toast.textContent = message;
  toast.className = 'toast ' + type;
  toast.classList.remove('hidden');
  setTimeout(() => {
    toast.classList.add('hidden');
  }, 3500);
}

// ===== 초기화 =====
document.addEventListener('DOMContentLoaded', () => {
  updateDate();

  // 프로그레스 바 애니메이션
  setTimeout(() => {
    const fills = document.querySelectorAll('.progress-fill');
    fills.forEach(fill => {
      const width = fill.style.width;
      fill.style.width = '0%';
      setTimeout(() => { fill.style.width = width; }, 100);
    });
  }, 300);

  // 환영 메시지
  setTimeout(() => {
    showToast('👋 닥터푸드에 오신 것을 환영합니다! AI 식단 추천 시스템이 준비되었습니다.', 'success');
  }, 1000);
});
