"""
uvicorn 00_http:app --reload
"""

from fastapi import FastAPI
from dataclasses import dataclass

app = FastAPI(
    title="First FastAPI",
    description="FastAPI 서버가 어떻게 시작되는지 확인하는 첫 예제입니다.",
    version="0.0.1",
)
# Model 
# 1. Memo
@dataclass
class Memo:
    id: int
    title: str
    content: str


# Mock Data
memos = []
memos.append(Memo(
        id=100,
        title="제목",
        content="배고파",
    ))
memos.append(Memo(
        id=101,
        title="제목",
        content="배고파",
    ))
memos.append(Memo(
        id=102,
        title="제목",
        content="배고파",
    ))



@app.get("/memo/get/{memo_id}")
def read_memo(memo_id: int)-> Memo:
    """  read_memo  """
    return 

@app.get("/memo/getall")
def read_all_memo() -> list[Memo]:
    """ read_all_memo """
    return memos

@app.post("/memo/create")
def create_memo(memo: Memo):
    """ create_memo """
    memos.append(memo)
    return 

@app.put("/memo/modify")
def modify_memo():
    """ modify_memo """
    return 

@app.delete("/memo/remove")
def remove_memo():
    """ remove_memo """
    return 



