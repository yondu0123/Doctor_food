import httpx
from typing import Dict, Any
from ..core.config import settings


class KakaoAuthService:
    """카카오 OAuth 인증 서비스"""
    
    TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"
    
    def __init__(self):
        self.client_id = settings.KAKAO_CLIENT_ID
        self.client_secret = settings.KAKAO_CLIENT_SECRET
    
    async def get_access_token(self, code: str, redirect_uri: str) -> str:
        """
        인가 코드로 액세스 토큰 받기
        
        Args:
            code: 카카오 인가 코드
            redirect_uri: 리다이렉트 URI
        
        Returns:
            액세스 토큰
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "code": code,
                    "redirect_uri": redirect_uri
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if response.status_code != 200:
                raise Exception(f"카카오 토큰 요청 실패: {response.text}")
            
            data = response.json()
            return data["access_token"]
    
    async def get_user_info(self, access_token: str) -> Dict[str, Any]:
        """
        액세스 토큰으로 사용자 정보 조회
        
        Args:
            access_token: 카카오 액세스 토큰
        
        Returns:
            사용자 정보 딕셔너리
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.USER_INFO_URL,
                headers={"Authorization": f"Bearer {access_token}"}
            )
            
            if response.status_code != 200:
                raise Exception(f"카카오 사용자 정보 요청 실패: {response.text}")
            
            data = response.json()
            
            # 필요한 정보만 추출
            kakao_account = data.get("kakao_account", {})
            profile = kakao_account.get("profile", {})
            
            return {
                "kakao_id": str(data["id"]),
                "email": kakao_account.get("email"),
                "nickname": profile.get("nickname"),
                "profile_image": profile.get("profile_image_url")
            }
    
    async def authenticate(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """
        카카오 OAuth 인증 전체 플로우
        
        Args:
            code: 카카오 인가 코드
            redirect_uri: 리다이렉트 URI
        
        Returns:
            사용자 정보
        """
        # 1. 액세스 토큰 받기
        access_token = await self.get_access_token(code, redirect_uri)
        
        # 2. 사용자 정보 조회
        user_info = await self.get_user_info(access_token)
        
        return user_info


# 싱글톤 인스턴스
_kakao_auth_service = None

def get_kakao_auth_service() -> KakaoAuthService:
    """카카오 인증 서비스 싱글톤 인스턴스 반환"""
    global _kakao_auth_service
    if _kakao_auth_service is None:
        _kakao_auth_service = KakaoAuthService()
    return _kakao_auth_service
