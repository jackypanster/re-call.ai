from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from app.services.auth_service import get_auth_service
from typing import Optional

router = APIRouter()

class SignUpRequest(BaseModel):
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/auth/signup")
async def signup(request: SignUpRequest, auth_service = Depends(get_auth_service)):
    """用户注册"""
    try:
        response = await auth_service.sign_up(request.email, request.password)
        user_id = None
        if response.get("user"):
            user_id = response["user"]["id"]
        elif hasattr(response, 'user') and response.user:
            user_id = response.user.id
            
        return {
            "success": True,
            "user_id": user_id,
            "message": "Registration successful"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/signin")
async def signin(request: SignInRequest, auth_service = Depends(get_auth_service)):
    """用户登录"""
    try:
        response = await auth_service.sign_in(request.email, request.password)
        
        # 处理不同的响应格式
        access_token = None
        user_id = None
        
        if response.get("session"):
            access_token = response["session"]["access_token"]
        elif hasattr(response, 'session') and response.session:
            access_token = response.session.access_token
            
        if response.get("user"):
            user_id = response["user"]["id"]
        elif hasattr(response, 'user') and response.user:
            user_id = response.user.id
            
        return {
            "success": True,
            "access_token": access_token,
            "user_id": user_id,
            "message": "Login successful"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# 依赖注入：获取当前用户
async def get_current_user(
    authorization: Optional[str] = Header(None),
    auth_service = Depends(get_auth_service)
):
    """从请求头获取当前用户"""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    
    try:
        # 从 "Bearer <token>" 中提取token
        token = authorization.split(" ")[1] if authorization.startswith("Bearer ") else authorization
        user_id = await auth_service.get_user_from_token(token)
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        return user_id
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/auth/me")
async def get_me(current_user: str = Depends(get_current_user)):
    """获取当前用户信息"""
    return {"user_id": current_user}
