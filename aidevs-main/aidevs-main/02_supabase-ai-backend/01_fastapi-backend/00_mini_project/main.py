"""
uvicorn main:app --reload
"""
from fastapi import FastAPI, HTTPException
from router.router_customer_cu import router_cu
from router.router_customer_rd import router_rd

app = FastAPI(
    title = "Request Test",
    description = "request test",
    version = "0.1"
)
app.include_router(router_cu)
app.include_router(router_rd)
