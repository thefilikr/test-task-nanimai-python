import httpx
from typing import Optional
import os

# TODO: Переделать на загрзку через конфиг. Неуспел( 
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://auth-service.local/validate")  # адрес сервиса авторизации
AUTH_SERVICE_SECRET = os.getenv("AUTH_SERVICE_SECRET", "supersecretkey")  # секретный ключ

async def validate_jwt_external(token: str) -> Optional[dict]:
    """
    Отправляет JWT токен во внешний сервис авторизации.
    Возвращает словарь с данными пользователя, если токен валиден, иначе None.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                AUTH_SERVICE_URL,
                json={"token": token},
                # Изначально планировал сделать тоже на jwt, т.к. слышал, что это сейчас 
                # считается более правильным и безопасным вариантом общения микросервисов.
                # Но не успеваю) 
                headers={"X-Auth-Secret": AUTH_SERVICE_SECRET},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
    return None