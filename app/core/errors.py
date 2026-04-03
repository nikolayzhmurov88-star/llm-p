class AppError(Exception):
    
    """
    Базовая ошибка приложения.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class ConflictError(AppError):
   
    """
    Конфликт: например, email уже существует.
    """

    def __init__(self, message: str = "Conflict") -> None:
        super().__init__(message)


class UnauthorizedError(AppError):
   
    """
    Неавторизован: неверный пароль, невалидный токен.
    """

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message)


class ForbiddenError(AppError):
    
    """
    Запрещено: нет прав.
    """

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message)


class NotFoundError(AppError):
    
    """
    Не найдено: объект в базе отсутствует.
    """

    def __init__(self, message: str = "Not found") -> None:
        super().__init__(message)


class ExternalServiceError(AppError):
    
    """
    Ошибка внешнего сервиса, например OpenRouter.
    """

    def __init__(self, message: str = "External service error") -> None:
        super().__init__(message)