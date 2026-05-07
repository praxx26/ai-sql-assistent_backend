from pydantic import BaseModel, SecretStr
import fastapi

class QueryRequest(BaseModel):
    host: str
    port: int
    user: str
    password: SecretStr
    database: str
    question: str