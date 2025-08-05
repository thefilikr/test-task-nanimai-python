from abc import ABC, abstractmethod

class IAuthService(ABC):
    @abstractmethod
    async def validate_jwt(self, token: str) -> bool:
        pass