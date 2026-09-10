"""Authentication service boundary. Replace with identity provider/JWT adapter in production."""

from fastapi import HTTPException, status

from app.schemas.auth import LoginRequest, LoginResponse


class AuthService:
    def login(self, payload: LoginRequest) -> LoginResponse:
        # Do not make this development token a production authentication mechanism.
        if not payload.username or not payload.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Thông tin đăng nhập không hợp lệ.")
        return LoginResponse(access_token="development-token", user={"username": payload.username, "name": "Nguyễn Minh An", "role": "Giám định viên"})


auth_service = AuthService()
