# FastAPI 문법 요약

## 기본 앱

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
 return {"message": "Hello FastAPI"}
```

## Path Parameter

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
 return {"user_id": user_id}
```

## Query Parameter

```python
@app.get("/search")
def search(keyword: str, limit: int = 10):
 return {"keyword": keyword, "limit": limit}
```

## Request Body

```python
from pydantic import BaseModel


class UserCreate(BaseModel):
 name: str
 age: int
```

## 예외 처리

```python
from fastapi import HTTPException

raise HTTPException(status_code=404, detail="Not found")
```

