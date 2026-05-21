from enum import Enum
from typing import List
from pydantic import BaseModel

class Role(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER"
    RISK_ANALYST = "RISK_ANALYST"
    PLATFORM_ADMIN = "PLATFORM_ADMIN"
    SYSTEM_AGENT = "SYSTEM_AGENT"

class User(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
    role: Role

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[Role] = None

from typing import Optional
