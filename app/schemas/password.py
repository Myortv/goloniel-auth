from pydantic import BaseModel, SecretStr

from app.utils.password import hash_password


class Password(BaseModel):
    password: SecretStr

    def hash_password(self):
        self.password = SecretStr(hash_password(self.password))
