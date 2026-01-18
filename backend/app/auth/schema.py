import uuid
from enum import Enum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from fastapi import HTTPException, status

class SecurityQuestionSchema(str, Enum):
    MOTHER_MAIDEN_NAME = "mother_maiden_name"
    CHILDHOOD_FRIEND = "childhood_friend"
    FAVORITE_COLOR = "favorite_color"
    BIRTHCITY = "birth_city"
    
    @classmethod
    def get_description(cls, value: "SecurityQuestionSchema") -> str:
        descriptions = {
            cls.MOTHER_MAIDEN_NAME: "What is your mother's maiden name?",
            cls.CHILDHOOD_FRIEND: "What is the name of your childhood friend?",
            cls.FAVORITE_COLOR: "What is your favorite color?",
            cls.BIRTHCITY: "In which city were you born?",
        }
        
        return descriptions.get(value, "Unknown security question")
    
class AccountStatusSchema(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    
class RoleChoiceSchema(str, Enum):
    CUSTOMER = "customer"
    ACCOUNT_EXECUTIVE = "account_executive"
    BRANCH_MANAGER = "branch_manager"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    TELLER = "teller"
    
class BaseUserSchema(SQLModel, table=False):
    username: str | None = Field(unique=True, default=None, max_length=12)
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    first_name: str = Field(max_length=30)
    middle_name: str | None = Field(default=None, max_length=30)
    last_name: str = Field(max_length=30)
    id_no: int = Field(unique=True, gt=0)
    is_active: bool = False
    is_superuser: bool = False
    security_question: SecurityQuestionSchema = Field(max_length=30)
    security_answer: str = Field(max_length=30)
    account_status: AccountStatusSchema = Field(default=AccountStatusSchema.INACTIVE)
    role: RoleChoiceSchema = Field(default=RoleChoiceSchema.CUSTOMER)
    
class UserCreateSchema(BaseUserSchema):
    password: str = Field(min_length=8, max_length=40)
    confirm_password: str = Field(min_length=8, max_length=40)
    
    @field_validator("confirm_password") 
    def validate_confirm_password(cls, v, values):
        if "password" in values.data and v!= values.data["password"]:
            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Password do not match",
                    "action": "Please ensure the password you enter match"
                }
            )
            
        return v
    
class UserReadSchema(BaseUserSchema):
    id: uuid.UUID
    full_name: str
    
class EmailRequestSchema(SQLModel, table=False):
    emai:EmailStr

class LoginRequestSchema(SQLModel, table=False):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=40
    )

class OTPVerifyRequestSchema(SQLModel, table=False):
    email: EmailStr
    otp:str = Field(
        min_length=6,
        max_length=6
    )