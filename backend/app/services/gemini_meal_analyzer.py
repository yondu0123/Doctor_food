import google.generativeai as genai
from PIL import Image
import json
import os
from typing import Dict, Any
from ..core.config import settings


class GeminiMealAnalyzer:
    """Gemini를 사용한 식사 사진 분석 서비스"""
    
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY가 설정되지 않았습니다.")
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_meal_photo(
        self, 
        photo_path: str, 
        patient_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        식사 사진을 분석하여 음식 종류, 영양소, 섭취량 등을 추정
        
        Args:
            photo_path: 사진 파일 경로
            patient_info: 환자 정보 (나이, 기저질환, 식이제한 등)
        
        Returns:
            분석 결과 딕셔너리
        """
        try:
            # 이미지 로드
            image = Image.open(photo_path)
            
            # 프롬프트 생성
            prompt = self._build_analysis_prompt(patient_info)
            
            # Gemini 분석 실행
            response = self.model.generate_content([prompt, image])
            
            # 응답 파싱
            result = self._parse_response(response.text)
            
            return result
            
        except Exception as e:
            print(f"Gemini 분석 오류: {str(e)}")
            return self._get_fallback_response()
    
    def _build_analysis_prompt(self, patient_info: Dict[str, Any]) -> str:
        """분석 프롬프트 생성"""
        
        conditions = patient_info.get('conditions', [])
        restrictions = patient_info.get('restrictions', [])
        allergies = patient_info.get('allergies', [])
        
        prompt = f"""
이 식사 사진을 분석해주세요.

[환자 정보]
- 나이: {patient_info.get('age', '알 수 없음')}세
- 기저질환: {', '.join(conditions) if conditions else '없음'}
- 식이제한: {', '.join(restrictions) if restrictions else '없음'}
- 알레르기: {', '.join(allergies) if allergies else '없음'}

[분석 요청]
1. 음식 종류 식별 (한국어로, 구체적으로)
2. 각 음식의 대략적인 양 추정
3. 총 칼로리 추정
4. 주요 영양소 추정 (단백질, 탄수화물, 지방, 나트륨)
5. 환자의 식이제한 준수 여부 평가
6. 섭취량 추정 (완식/반/1/3/미섭취)

[출력 형식]
반드시 다음 JSON 형식으로만 출력하세요 (마크다운 코드블록 없이):
{{
  "foods": [
    {{"name": "현미밥", "amount": "1공기 (210g)", "calories": 300}},
    {{"name": "된장국", "amount": "1그릇 (200ml)", "calories": 50}},
    {{"name": "생선구이", "amount": "1토막 (80g)", "calories": 120}}
  ],
  "total_nutrition": {{
    "calories": 520,
    "protein": 25.5,
    "carbs": 70.2,
    "fat": 12.3,
    "sodium": 850
  }},
  "portion_consumed": "full",
  "dietary_compliance": {{
    "status": "good",
    "issues": [],
    "notes": "저염식 기준 적합, 단백질 적정량"
  }},
  "confidence": 0.85
}}

주의사항:
- 음식 이름은 한국어로 정확하게
- 칼로리와 영양소는 실제 음식량 기준으로 추정
- confidence는 0.0~1.0 사이 값
- 식이제한 위반 시 issues 배열에 구체적으로 명시
"""
        return prompt
    
    def _parse_response(self, text: str) -> Dict[str, Any]:
        """Gemini 응답을 JSON으로 파싱"""
        try:
            # 마크다운 코드블록 제거
            text = text.strip()
            if text.startswith('```json'):
                text = text[7:]
            if text.startswith('```'):
                text = text[3:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            # JSON 파싱
            result = json.loads(text)
            
            # 필수 필드 검증
            required_fields = ['foods', 'total_nutrition', 'portion_consumed', 'dietary_compliance', 'confidence']
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"필수 필드 누락: {field}")
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"JSON 파싱 오류: {str(e)}")
            print(f"원본 텍스트: {text}")
            return self._get_fallback_response()
        except Exception as e:
            print(f"응답 파싱 오류: {str(e)}")
            return self._get_fallback_response()
    
    def _get_fallback_response(self) -> Dict[str, Any]:
        """분석 실패 시 기본 응답"""
        return {
            "foods": [
                {"name": "분석 실패", "amount": "알 수 없음", "calories": 0}
            ],
            "total_nutrition": {
                "calories": 0,
                "protein": 0.0,
                "carbs": 0.0,
                "fat": 0.0,
                "sodium": 0
            },
            "portion_consumed": "unknown",
            "dietary_compliance": {
                "status": "unknown",
                "issues": ["AI 분석 실패"],
                "notes": "수동으로 입력해주세요"
            },
            "confidence": 0.0
        }


# 싱글톤 인스턴스
_analyzer_instance = None

def get_meal_analyzer() -> GeminiMealAnalyzer:
    """Gemini 분석기 싱글톤 인스턴스 반환"""
    global _analyzer_instance
    if _analyzer_instance is None:
        _analyzer_instance = GeminiMealAnalyzer()
    return _analyzer_instance
