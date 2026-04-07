from app.core.security import create_access_token, get_password_hash, verify_password
from app.core.errors import (ConflictError, UnauthorizedError, NotFoundError)
from app.repositories.users import UserRepository
from app.db.models import User
from app.core.config import settings 

class AuthUseCase:

    """Бизнес-логика аутентификации"""
    
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    

    async def register(self, email: str, password: str, role: str = "user") -> User:

        """Регистрация"""

        if await self.user_repo.get_by_email(email):
            raise ConflictError(f"Email {email} already exists")
        
        hashed_password = get_password_hash(password)

        user = User(
        email=email,
        password_hash=hashed_password,
        role=role,
        )

        created_user = await self.user_repo.create(user) 
        return created_user
   

    async def login(self, email: str, password: str) -> str:

        """Логин"""

        user = await self.user_repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid credentials")
        
        access_token = create_access_token(
        sub=str(user.id),
        role=user.role,
        expires_minutes=settings.access_token_expire_minutes, 
        )
        
        return access_token
    
    
    async def get_profile(self, user_id: int) -> User:

        """Профиль"""

        user = await self.user_repo.get_by_id(user_id)
        
        if not user:
            raise NotFoundError(f"User {user_id} not found")
        
        return user