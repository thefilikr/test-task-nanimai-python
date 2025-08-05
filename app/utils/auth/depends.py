from fastapi import Depends, HTTPException, status, Request
from .service import AuthService

# auth_service = AuthService()

# async def get_current_user(request: Request):
#     auth_header = request.headers.get("Authorization")
#     if not auth_header or not auth_header.startswith("Bearer "):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing JWT token")
#     token = auth_header.split(" ", 1)[1]
#     user_data = await auth_service.validate_jwt(token)
#     if not user_data or not user_data.get("is_valid"):
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid JWT token")
#     return user_data


async def get_current_user(request: Request):
    # MOCK: всегда возвращаем тестового пользователя (id=1, is_admin=True)
    return {"id": "1", "is_admin": True, "is_valid": True}