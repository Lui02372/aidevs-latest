-- [학습] 앱 전용 이름 공간을 만든다. IF NOT EXISTS는 이미 존재할 때 생성을 건너뛴다.
CREATE SCHEMA IF NOT EXISTS simple_multi_llm;

-- [학습] 여행 메모 테이블이다. 기존 테이블의 구조를 자동 수정하는 migration은 아니다.
CREATE TABLE IF NOT EXISTS simple_multi_llm.notes (
    -- [학습] BIGSERIAL은 큰 정수 ID를 자동 부여하고 PRIMARY KEY는 행을 유일하게 식별한다.
    id BIGSERIAL PRIMARY KEY,
    -- [학습] 이름과 메시지 길이는 API NoteRequest의 제한과 대응하며 NOT NULL은 값 누락을 막는다.
    name VARCHAR(50) NOT NULL,
    message VARCHAR(500) NOT NULL,
    -- [학습] 시간대가 있는 생성 시각을 DB의 NOW() 기본값으로 기록한다.
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- [학습] 채팅은 질문과 답변을 각각 한 행으로 저장하며 세션 ID로 묶는다.
CREATE TABLE IF NOT EXISTS simple_multi_llm.chat_messages (
    id BIGSERIAL PRIMARY KEY,
    -- [학습] 세션 문자열은 사용자 계정 외래 키가 아니다. 별도 사용자 테이블이나 소유권 검사는 없다.
    session_id VARCHAR(100) NOT NULL,
    -- [학습] CHECK 제약은 역할이 user 또는 assistant인 행만 허용한다.
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    -- [학습] TEXT는 대화 본문, created_at은 저장 시각이다. 모델명이나 공급자 열은 없다.
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- [학습] 세션 필터와 id 정렬 조회에 사용할 복합 인덱스를 만든다. 실제 사용 여부는 DB 실행 계획으로 별도 확인한다.
CREATE INDEX IF NOT EXISTS idx_chat_messages_session
ON simple_multi_llm.chat_messages (session_id, id);
