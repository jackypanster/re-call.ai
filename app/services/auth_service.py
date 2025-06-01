from supabase import create_client
from app.config import settings
import logging

class AuthService:
    def __init__(self):
        # 检查是否有有效的Supabase配置
        if (settings.supabase_url and 
            settings.supabase_key and 
            settings.supabase_url.startswith("https://") and
            not settings.supabase_url.endswith(".supabase.co") == False):
            try:
                self.client = create_client(settings.supabase_url, settings.supabase_key)
                logging.info("Supabase Auth client initialized successfully")
            except Exception as e:
                self.client = None
                logging.warning(f"Failed to initialize Supabase client: {e}")
        else:
            self.client = None
            logging.warning("Supabase Auth not configured - using demo mode")

    async def sign_up(self, email: str, password: str):
        """用户注册"""
        if not self.client:
            return {"user": {"id": f"demo-{email}"}, "session": None}
            
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            logging.error(f"Sign up error: {e}")
            raise

    async def sign_in(self, email: str, password: str):
        """用户登录"""
        if not self.client:
            return {
                "user": {"id": f"demo-{email}"},
                "session": {"access_token": f"demo-token-{email}"}
            }
            
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return response
        except Exception as e:
            logging.error(f"Sign in error: {e}")
            raise

    async def verify_token(self, token: str):
        """验证token"""
        if not self.client:
            # Demo mode - 从token中提取用户ID
            if token.startswith("demo-token-"):
                email = token.replace("demo-token-", "")
                return {"user": {"id": f"demo-{email}"}}
            return None
            
        try:
            response = self.client.auth.get_user(token)
            return response
        except Exception as e:
            logging.error(f"Token verification error: {e}")
            return None

    async def get_user_from_token(self, token: str):
        """从token获取用户信息"""
        user_response = await self.verify_token(token)
        if user_response and user_response.get("user"):
            return user_response["user"]["id"]
        return None

# 单例
auth_service = AuthService()

def get_auth_service():
    return auth_service 