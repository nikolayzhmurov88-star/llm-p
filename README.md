# Построение защищённого API для работы с большой языковой моделью
# llm-p

FastAPI-сервис с JWT‑аутентификацией, SQLite и проксированием запросов к LLM через OpenRouter.

## Требования

- Python 3.11 или выше.
- Установленный `uv`.

## Установка `uv`

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Проверка установки:

```bash
uv --version
```

## Клонирование проекта

```bash
git clone https://github.com/nikolayzhmurov88-star/llm-p.git
cd llm-p
```

## Настройка переменных окружения

1. Скопируйте пример `.env`:

   ```bash
   cp .env.example .env
   ```

2. Получите OpenRouter API key:

   - перейдите на [https://openrouter.ai/keys](https://openrouter.ai/keys);
   - войдите в аккаунт;
   - в разделе **Keys** нажмите **Create Key**;
   - скопируйте ключ (вида `sk-or-v1-...`).

3. Вставьте API key в `.env` одной командой:

   ```bash
   echo "" >> .env 
   echo "OPENROUTER_API_KEY=sk-or-v1-ваш_ключ_здесь" >> .env
   ```

   Где `ваш_ключ_здесь` — это скопированный ключ.

## Создание виртуального окружения

```bash
uv venv
```

После выполнения команды будет создано виртуальное окружение в папке `.venv`.

## Установка зависимостей из pyproject.toml

```bash
uv pip compile pyproject.toml -o requirements.txt
uv pip install -r requirements.txt


## Запуск приложения

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу:

**Swagger UI:** http://127.0.0.1:8000/docs  