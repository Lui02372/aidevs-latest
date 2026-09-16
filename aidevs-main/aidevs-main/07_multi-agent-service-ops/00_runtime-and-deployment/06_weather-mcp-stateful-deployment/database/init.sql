CREATE SCHEMA IF NOT EXISTS weather_agent;
CREATE TABLE IF NOT EXISTS weather_agent.runs (
    run_id UUID PRIMARY KEY,
    city TEXT NOT NULL,
    requested_day TEXT NOT NULL,
    provider TEXT NOT NULL,
    model TEXT NOT NULL,
    tool_result JSONB NOT NULL,
    answer TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
