from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(
        ..., min_length=8, max_length=72
    )  # Enforce password length constraints
    role: str = Field("employee", pattern="^(admin|engineer|employee)$")


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str

    class Config:
        orm_mode = True
