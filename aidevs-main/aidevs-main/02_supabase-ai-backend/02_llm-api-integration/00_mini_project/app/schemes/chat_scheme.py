# ChatRequest.py
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    user_id:str = Field(min_length=1, examples=["id01"])
    prompt:str =Field(min_length=1, examples=["안녕 !"])

class ChatResponse(BaseModel):
    answer:str =Field(min_length=1, examples=["안녕 !"])