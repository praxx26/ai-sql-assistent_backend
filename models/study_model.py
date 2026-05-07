from pydantic import BaseModel

class StudyQueryRequest(BaseModel):
    question:str