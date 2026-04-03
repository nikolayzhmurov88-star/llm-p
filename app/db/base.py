from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    
    """
    Базовый класс декларативных моделей SQLAlchemy.
    ORM‑модели приложения должны наследоваться от этого класса.
    """

    pass