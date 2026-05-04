from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..models.user import User, UserRole
from ..schemas.auth import UserRegister, UserLogin, Token, UserResponse, OAuthLogin
from ..auth.jwt import get_password_hash, verify_password, create_access_token
from ..auth.dependencies import get_current_user
from ..services.kakao_auth import get_kakao_auth_service

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    이메일/비밀번호 회원가입
    
    - 이메일 중복 체크
    - 비밀번호 해싱
    - 사용자 생성
    """
    
    # 이메일 중복 체크
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다"
        )
    
    # 사용자명 생성 (이메일 앞부분 사용)
    username = user_data.email.split('@')[0]
    
    # 사용자명 중복 시 숫자 추가
    base_username = username
    counter = 1
    while db.query(User).filter(User.username == username).first():
        username = f"{base_username}{counter}"
        counter += 1
    
    # 비밀번호 해싱
    hashed_password = get_password_hash(user_data.password)
    
    # 사용자 생성
    new_user = User(
        email=user_data.email,
        username=username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        phone=user_data.phone,
        role=user_data.role,
        oauth_provider="email"  # 이메일 가입
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    이메일/비밀번호 로그인
    
    - 사용자 조회
    - 비밀번호 검증
    - JWT 토큰 발급
    """
    
    # 사용자 조회
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다"
        )
    
    # OAuth 사용자는 이메일 로그인 불가
    if user.oauth_provider != "email":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{user.oauth_provider} 계정입니다. 소셜 로그인을 사용해주세요."
        )
    
    # 비밀번호 검증
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다"
        )
    
    # 활성 사용자 체크
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 계정입니다"
        )
    
    # JWT 토큰 생성
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    현재 로그인한 사용자 정보 조회
    """
    return current_user


@router.post("/logout")
async def logout():
    """
    로그아웃 (클라이언트에서 토큰 삭제)
    """
    return {"message": "로그아웃 되었습니다"}


@router.post("/kakao", response_model=Token)
async def kakao_login(oauth_data: OAuthLogin, db: Session = Depends(get_db)):
    """
    카카오 OAuth 로그인
    
    - 카카오 인가 코드로 사용자 정보 조회
    - 기존 사용자면 로그인, 신규면 자동 가입
    - JWT 토큰 발급
    """
    
    try:
        # 카카오 인증 서비스
        kakao_service = get_kakao_auth_service()
        
        # 카카오 사용자 정보 조회
        kakao_user = await kakao_service.authenticate(
            code=oauth_data.code,
            redirect_uri=oauth_data.redirect_uri
        )
        
        # 카카오 ID로 기존 사용자 조회
        user = db.query(User).filter(
            User.oauth_provider == "kakao",
            User.oauth_id == kakao_user["kakao_id"]
        ).first()
        
        # 신규 사용자면 자동 가입
        if not user:
            # 이메일로도 확인 (이메일 계정이 있을 수 있음)
            email_user = db.query(User).filter(User.email == kakao_user["email"]).first()
            
            if email_user:
                # 기존 이메일 계정이 있으면 카카오 연동
                email_user.oauth_provider = "kakao"
                email_user.oauth_id = kakao_user["kakao_id"]
                email_user.profile_image = kakao_user["profile_image"]
                user = email_user
            else:
                # 완전 신규 사용자 생성
                username = kakao_user["nickname"] or kakao_user["email"].split('@')[0]
                
                # 사용자명 중복 체크
                base_username = username
                counter = 1
                while db.query(User).filter(User.username == username).first():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User(
                    email=kakao_user["email"],
                    username=username,
                    full_name=kakao_user["nickname"],
                    oauth_provider="kakao",
                    oauth_id=kakao_user["kakao_id"],
                    profile_image=kakao_user["profile_image"],
                    role=UserRole.GUARDIAN  # 기본 역할: 보호자
                )
                
                db.add(user)
            
            db.commit()
            db.refresh(user)
        
        # JWT 토큰 생성
        access_token = create_access_token(data={"sub": user.username})
        
        return {"access_token": access_token, "token_type": "bearer"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"카카오 로그인 실패: {str(e)}"
        )
