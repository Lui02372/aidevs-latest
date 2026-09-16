from typing import Any

from pydantic import BaseModel, Field

class Customer(BaseModel):
    id:str = Field(min_length=3, examples=["id01"])
    pwd:str = Field(min_length=4, examples=["pwd01"])
    name:str = Field(min_length=5, examples=["james"])
    age:int = Field(ge=1, examples=[20])

class CustomerDetail(BaseModel):
    id:str = Field(min_length=3, examples=["id01"])
    name:str = Field(min_length=5, examples=["james"])
    age:int = Field(ge=1, examples=[20])    