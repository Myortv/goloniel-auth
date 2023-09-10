from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class LoginForm(BaseModel):
    secret: str = Field(..., min_length=8)
