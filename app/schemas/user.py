import re

from typing import Optional, List

from pydantic import BaseModel, validator, SecretStr

from app.utils.password import hash_password

email = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

# class UserInDB(BaseModel):
#     id: int
#     login: str
#     password: str
#     discord_id: Optional[str] = None


class UserInDBProtected(BaseModel):
    id: int
    username: str
    discord_id: Optional[str] = None
    role: Optional[str] = None
    emails: Optional[List[str]] = []

    @validator('emails')
    def validate_emails(cls, v):
        if not v:
            return v
        for email_addr_to_check in v:
            if email.match(email_addr_to_check):
                return v
            else:
                raise ValueError(
                    f'Your email entry {v} not valid!'
                )


class UserCreateProtected(BaseModel):
    username: str
    password: SecretStr

    def hash_password(self):
        self.password = hash_password(str(self.password))


class UserUpdateProtected(BaseModel):
    username: str
    emails: Optional[List[str]] = []


class UserInDBWithPassword(UserInDBProtected):
    password: SecretStr
