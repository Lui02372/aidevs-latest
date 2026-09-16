CREATE SCHEMA IF NOT EXISTS simple_multi_llm;

CREATE TABLE IF NOT EXISTS simple_multi_llm.notes (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    message VARCHAR(500) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS simple_multi_llm.chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session
ON simple_multi_llm.chat_messages (session_id, id);
