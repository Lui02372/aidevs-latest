"""
시나리오
사용자가 도시·날짜·Cloud LLM을 선택하면 Backend가 run_id를 만들고 Redis에 진행 상태를
기록합니다. Cache에 날씨가 없으면 Weather MCP로 실제 데이터를 조회하고 LLM이 답변을
작성합니다. 완료 결과는 PostgreSQL에 영구 저장하며 Readiness는 각 의존성을 구분합니다.
"""
import json
import os
from contextlib import asynccontextmanager
from typing import Literal
from uuid import UUID, uuid4

import psycopg
import redis
from fastapi import BackgroundTasks, FastAPI, HTTPException
from google import genai
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI
from psycopg.rows import dict_row
from pydantic import BaseModel, Field

MCP_URL = os.getenv("WEATHER_MCP_URL", "http://127.0.0.1:8010/mcp")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://agent_user:agent_pwd@127.0.0.1:5433/agent_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
CACHE_TTL = int(os.getenv("WEATHER_CACHE_TTL_SECONDS", "600"))
app = FastAPI(title="Stateful Weather MCP Agent", version="1.0.0")

class WeatherRequest(BaseModel):
    city: str = Field(min_length=1, max_length=60)
    day: Literal["today", "tomorrow"] = "tomorrow"
    provider: Literal["openai", "gemini"] = "openai"

class StateStore:
    def __init__(self): self.client = redis.from_url(REDIS_URL, decode_responses=True)
    def ping(self): return bool(self.client.ping())
    def progress(self, run_id, percent, stage, message):
        key = f"weather:run:{run_id}"
        self.client.hset(key, mapping={"run_id": run_id, "progress": percent, "stage": stage, "message": message})
        self.client.expire(key, 3600)
    def get_progress(self, run_id): return self.client.hgetall(f"weather:run:{run_id}")
    def cached_weather(self, city, day):
        value = self.client.get(f"weather:cache:{city.strip().lower()}:{day}")
        return json.loads(value) if value else None
    def cache_weather(self, city, day, value):
        self.client.setex(f"weather:cache:{city.strip().lower()}:{day}", CACHE_TTL, json.dumps(value, ensure_ascii=False))

class RunRepository:
    def ping(self):
        with psycopg.connect(DATABASE_URL) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)
    def schema_ready(self):
        with psycopg.connect(DATABASE_URL) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT to_regclass('weather_agent.runs')")
            return cursor.fetchone()[0] is not None
    def save(self, run_id, payload, model, tool_result, answer):
        with psycopg.connect(DATABASE_URL) as connection, connection.cursor() as cursor:
            cursor.execute("INSERT INTO weather_agent.runs (run_id, city, requested_day, provider, model, tool_result, answer) VALUES (%s,%s,%s,%s,%s,%s,%s)", (UUID(run_id), payload.city, payload.day, payload.provider, model, json.dumps(tool_result), answer))
    def list_runs(self, limit=20):
        with psycopg.connect(DATABASE_URL, row_factory=dict_row) as connection, connection.cursor() as cursor:
            cursor.execute("SELECT run_id, city, requested_day, provider, model, tool_result, answer, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT %s", (limit,))
            return [dict(row) for row in cursor.fetchall()]

state_store = StateStore()
repository = RunRepository()

@asynccontextmanager
async def mcp_session():
    async with streamable_http_client(MCP_URL) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session

async def call_weather_tool(city, day):
    async with mcp_session() as session:
        result = await session.call_tool("get_weather", {"city": city, "day": day})
        text = "\n".join(item.text for item in result.content if hasattr(item, "text"))
        if result.isError: raise RuntimeError(text or "Weather MCP Tool 호출 실패")
        return json.loads(text)

def generate_answer(provider, weather):
    prompt = "다음 실제 날씨만 근거로 한국어 3문장 이내의 날씨와 옷차림을 설명하세요.\n" + json.dumps(weather, ensure_ascii=False)
    if provider == "openai":
        if not os.getenv("OPENAI_API_KEY"): raise RuntimeError("OPENAI_API_KEY를 설정하세요.")
        model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        return OpenAI().responses.create(model=model, input=prompt).output_text, model
    if not os.getenv("GEMINI_API_KEY"): raise RuntimeError("GEMINI_API_KEY를 설정하세요.")
    model = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
    response = genai.Client(api_key=os.environ["GEMINI_API_KEY"]).models.generate_content(model=model, contents=prompt)
    return response.text or "응답 내용이 없습니다.", model

@app.get("/health/live")
def live(): return {"status": "ok", "service": "backend"}

@app.get("/health/ready")
async def ready():
    checks = {"redis": False, "database": False, "database_schema": False, "mcp": False}
    errors = {}
    for name, check in (("redis", state_store.ping), ("database", repository.ping), ("database_schema", repository.schema_ready)):
        try: checks[name] = check()
        except Exception as error: errors[name] = str(error)
    try:
        async with mcp_session() as session:
            checks["mcp"] = "get_weather" in [tool.name for tool in (await session.list_tools()).tools]
    except Exception as error: errors["mcp"] = str(error)
    if not all(checks.values()): raise HTTPException(503, detail={"status": "degraded", "checks": checks, "errors": errors})
    return {"status": "ok", "checks": checks}

async def execute_weather_agent(run_id: str, payload: WeatherRequest):
    try:
        tool_result = state_store.cached_weather(payload.city, payload.day)
        cache_hit = tool_result is not None
        if tool_result is None:
            state_store.progress(run_id, 35, "weather_tool", "Weather MCP에서 날씨를 조회합니다.")
            tool_result = await call_weather_tool(payload.city, payload.day)
            if not tool_result.get("success"): raise ValueError(f"날씨 조회 실패: {tool_result}")
            state_store.cache_weather(payload.city, payload.day, tool_result)
        else: state_store.progress(run_id, 35, "cache", "Redis Cache의 날씨를 사용합니다.")
        state_store.progress(run_id, 70, "llm", f"{payload.provider}가 답변을 작성합니다.")
        answer, model = generate_answer(payload.provider, tool_result)
        repository.save(run_id, payload, model, tool_result, answer)
        state_store.progress(run_id, 100, "completed", json.dumps({"answer": answer, "provider": payload.provider, "model": model, "tool": "get_weather", "cache_hit": cache_hit, "tool_result": tool_result}, ensure_ascii=False))
    except Exception as error:
        try: state_store.progress(run_id, 100, "failed", str(error))
        except Exception: pass

@app.post("/api/weather", status_code=202)
async def weather_agent(payload: WeatherRequest, background_tasks: BackgroundTasks):
    run_id = str(uuid4())
    state_store.progress(run_id, 5, "queued", "실행 대기열에 등록했습니다.")
    background_tasks.add_task(execute_weather_agent, run_id, payload)
    return {"run_id": run_id, "status": "queued"}

@app.get("/api/runs/{run_id}/progress")
def progress(run_id: str):
    result = state_store.get_progress(run_id)
    if not result: raise HTTPException(404, detail="진행 상태가 없거나 TTL이 만료되었습니다.")
    result["progress"] = int(result["progress"])
    if result["stage"] == "completed":
        result["result"] = json.loads(result["message"])
        result["message"] = "PostgreSQL에 실행 이력을 저장했습니다."
    return result

@app.get("/api/runs")
def runs(): return {"runs": repository.list_runs()}
