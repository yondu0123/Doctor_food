// 닥터푸드 관리자 대시보드 JavaScript

// 페이지 전환 함수
function showPage(pageId) {
  // 모든 페이지 숨기기
  document.querySelectorAll('.page').forEach(page => {
    page.classList.remove('active');
  });
  
  // 모든 네비게이션 아이템 비활성화
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.remove('active');
  });
  
  // 선택된 페이지 표시
  const selectedPage = document.getElementById(`page-${pageId}`);
  if (selectedPage) {
    selectedPage.classList.add('active');
  }
  
  // 선택된 네비게이션 아이템 활성화
  event.currentTarget.classList.add('active');
  
  // 페이지 제목 업데이트
  const titles = {
    'dashboard': '대시보드',
    'patients': '환자 관리',
    'ai-diet': 'AI 식단 추천',
    'medication': '투약 관리',
    'guardian': '보호자 알림',
    'ingredients': '식자재 관리'
  };
  
  document.getElementById('page-title').textContent = titles[pageId] || '대시보드';
}

// 날짜 표시
function updateDate() {
  const now = new Date();
  const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
  const dateStr = now.toLocaleDateString('ko-KR', options);
  const dateElement = document.getElementById('page-date');
  if (dateElement) {
    dateElement.textContent = dateStr;
  }
}

// 알림 표시
function showNotification() {
  showToast('알림 3개가 있습니다', 'info');
}

// 토스트 메시지
function showToast(message, type = 'info') {
  const toast = document.getElementById('toast');
  if (toast) {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
      toast.classList.add('hidden');
    }, 3000);
  }
}

// AI 식단 생성
function generateAIDiet() {
  const modal = document.getElementById('ai-modal');
  if (modal) {
    modal.classList.remove('hidden');
    
    // 단계별 진행 시뮬레이션
    const steps = ['step1', 'step2', 'step3', 'step4', 'step5'];
    let currentStep = 0;
    
    const interval = setInterval(() => {
      if (currentStep < steps.length) {
        const stepElement = document.getElementById(steps[currentStep]);
        if (stepElement) {
          stepElement.classList.add('active');
          stepElement.textContent = stepElement.textContent.replace('⏳', '✅');
        }
        currentStep++;
      } else {
        clearInterval(interval);
        setTimeout(() => {
          modal.classList.add('hidden');
          showToast('AI 식단 생성이 완료되었습니다!', 'success');
        }, 500);
      }
    }, 800);
  }
}

// 환자 필터링
function filterPatients(type) {
  // 필터 버튼 활성화
  document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.classList.remove('active');
  });
  event.currentTarget.classList.add('active');
  
  showToast(`${type} 필터가 적용되었습니다`, 'info');
}

// 환자 상세 정보
function showPatientDetail(name) {
  showToast(`${name} 어르신의 상세 정보를 불러오는 중...`, 'info');
}

// 환자 추가
function openAddPatient() {
  showToast('환자 추가 기능은 준비 중입니다', 'info');
}

// 투약 완료 표시
function markMedDone(patientName, time) {
  showToast(`${patientName} 어르신 ${time} 투약이 완료되었습니다`, 'success');
  event.currentTarget.closest('.med-patient-card').classList.remove('missed');
  event.currentTarget.closest('.med-patient-card').classList.add('done');
}

// 보호자 메시지 답장
function sendReply() {
  const input = event.currentTarget.previousElementSibling;
  if (input && input.value.trim()) {
    showToast('답장이 전송되었습니다', 'success');
    input.value = '';
  }
}

// 일일 리포트 전송
function sendDailyReport() {
  showToast('전체 보호자에게 일일 리포트를 전송했습니다', 'success');
}

// 주간 식단 변경
function changeWeek(direction) {
  showToast(`${direction > 0 ? '다음' : '이전'} 주 식단을 불러오는 중...`, 'info');
}

// 페이지 로드 시 초기화
document.addEventListener('DOMContentLoaded', function() {
  updateDate();
  
  // 날짜 자동 업데이트 (1분마다)
  setInterval(updateDate, 60000);
});
