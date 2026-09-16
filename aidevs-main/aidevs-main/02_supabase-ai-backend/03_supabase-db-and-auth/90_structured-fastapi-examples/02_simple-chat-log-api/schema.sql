-- 02_simple-chat-log-api 예제에서 사용하는 테이블입니다.
--
-- 이 예제의 목표:
-- 1. 사용자의 질문과 AI 답변을 한 테이블에 저장합니다.
-- 2. 아직 로그인 사용자 구분은 하지 않습니다.
-- 3. Gemini가 생성한 답변을 저장합니다.

create table if not exists ex90_simple_chat_logs (
  -- 로그 1건을 구분하는 고유 id입니다.
  id uuid primary key default gen_random_uuid(),

  -- 사용자가 보낸 질문과 서버가 만든 답변입니다.
  user_message text not null,
  assistant_message text,

  -- provider/model은 응답 출처를 구분할 때 사용합니다.
  provider text not null default 'gemini',
  model text,

  -- 실제 외부 AI API를 호출했는지 표시합니다.
  actual_api_called boolean not null default false,

  -- 성공/실패 상태와 실패 시 오류 메시지를 저장합니다.
  status text not null default 'success',
  error_message text,

  -- 로그가 만들어진 시간입니다.
  created_at timestamp not null default now()
);
