from .interfaces import IAuthService
from .external_jwt import validate_jwt_external

class AuthService(IAuthService):
    async def validate_jwt(self, token: str) -> dict:
        """
        Возвращает данные пользователя, если токен валиден, иначе None.
        """
        return await validate_jwt_external(token)