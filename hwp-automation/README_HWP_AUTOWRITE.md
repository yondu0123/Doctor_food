# HWP 특정섹션 자동삽입

## 1) Windows (권장)
필수:
- Windows + 한글(HWP)
- Python + `pip install pywin32`

실행:
```bash
python hwp_section_writer_windows.py \
  --hwp "C:\\path\\양식_초기창업팀_신청서_및_사업계획서_작성_양식.hwp" \
  --sections "C:\\path\\sections.json" \
  --save-as "C:\\path\\양식_자동작성완료.hwp"
```

동작:
- 제목 키워드(`1-1...`, `2-2...`, `3-2...`) 검색
- 해당 줄 바로 아래에 본문 삽입
- 저장
- 원본 백업(`*.backup.hwp`) 생성

## 2) macOS (fallback)
필수:
- Hanword 설치
- 시스템 설정 > 개인정보 보호 및 보안 > 손쉬운 사용에서 Terminal/Code 권한 허용

실행:
```bash
osascript hwp_section_writer_macos.applescript \
  "/절대경로/양식.hwp" \
  "/절대경로/sections.json"
```

주의:
- UI 자동화라 포커스가 바뀌면 실패할 수 있음
- Windows COM 방식보다 안정성이 떨어짐
