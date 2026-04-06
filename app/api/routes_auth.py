from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.errors import ConflictError, UnauthorizedError, NotFoundError
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase
from app.api.deps import get_auth_usecase, get_current_user_id


router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    response_model=UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
)
async def register(
    request: RegisterRequest,
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
) -> UserPublic:
    
    """
    Регистрация нового пользователя.

    - **email**: Email пользователя (должен быть уникальным)
    - **password**: Пароль (от 8 до 128 символов)
    """

    try:
        user = await auth_usecase.register(
            email=request.email,
            password=request.password,
            role="user",
        )
        return UserPublic.model_validate(user)
    except ConflictError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e.message),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Аутентификация пользователя",
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
) -> TokenResponse:
    
    """
    Аутентификация пользователя и получение JWT токена.

    Использует OAuth2 стандарт для интеграции со Swagger UI.
    - **username**: Email пользователя
    - **password**: Пароль пользователя
    """
    
    try:
        access_token = await auth_usecase.login(
            email=form_data.username,
            password=form_data.password,
        )
        return TokenResponse(access_token=access_token)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.message),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get(
    "/me",
    response_model=UserPublic,
    summary="Получение профиля текущего пользователя",
)
async def get_me(
    user_id: int = Depends(get_current_user_id),
    auth_usecase: AuthUseCase = Depends(get_auth_usecase),
) -> UserPublic:
    """
    Возвращает информацию о текущем аутентифицированном пользователе.
    """
    try:
        user = await auth_usecase.get_profile(user_id)
        return UserPublic.model_validate(user)
    except NotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e.message),
        )