# 04 RAG

RAG는 질문에 바로 답하지 않고 관련 문서를 먼저 찾은 다음, 그 문서를 근거로
LLM이 답하도록 만드는 방식입니다.

```text
질문 → 관련 문서 검색 → Context 구성 → Ollama 답변 → 출처 표시
```

## 학습 순서

### 1단계 · Python만 사용

| 파일 | 학습 내용 |
| --- | --- |
| `01_rag_concept.py` | RAG 전체 흐름 |
| `02_document_chunk.py` | 문서 Chunk와 출처 |
| `03_keyword_search.py` | 키워드 검색과 top_k |
| `04_vector_search.py` | 벡터와 코사인 유사도 |
| `05_grounded_answer.py` | Context 기반 답변과 답변 제한 |

```powershell
cd C:\aidevs\05_llm-agent-orchestration\04_rag
python .\01_rag_concept.py
python .\02_document_chunk.py
python .\03_keyword_search.py
python .\04_vector_search.py
python .\05_grounded_answer.py
```

### 2단계 · 실제 RAG

| 파일 | 학습 내용 |
| --- | --- |
| `06_pgvector_index_and_search.py` | Ollama Embedding, pgvector 저장과 검색 |
| `07_ollama_rag_answer.py` | 검색 Context로 Ollama 답변 생성 |
| `08_rag_cache.py` | 동일 질문의 Redis MISS와 HIT |

06을 먼저 실행해야 07과 08에서 검색할 문서가 준비됩니다.

```powershell
python .\06_pgvector_index_and_search.py
python .\07_ollama_rag_answer.py
python .\08_rag_cache.py
```

### 3단계 · PDF RAG

| 파일 | 학습 내용 |
| --- | --- |
| `09_01_pdf_index.py` | PDF 읽기, Chunk 생성, pgvector 저장 |
| `09_02_pdf_search.py` | PDF Chunk 유사도 검색 |
| `09_03_pdf_rag_ollama.py` | PDF Context로 Ollama 답변 생성 |
| `09_04_pdf_rag_cache.py` | PDF 답변을 Redis에 Cache |

PDF 과정도 반드시 09-01부터 순서대로 실행합니다.

```powershell
python .\09_01_pdf_index.py
python .\09_02_pdf_search.py
python .\09_03_pdf_rag_ollama.py
python .\09_04_pdf_rag_cache.py
```

기본 PDF 파일은 같은 디렉터리의 `ai.pdf`입니다. 다른 파일을 사용하려면
`09_01_pdf_index.py` 위쪽의 `PDF_PATH`를 수정합니다.

## 필요한 실행 환경

01~05는 외부 서비스 없이 실행할 수 있습니다. 06부터는 다음 서비스가 필요합니다.

- Ollama: `127.0.0.1:11434`
- PostgreSQL/pgvector: `127.0.0.1:5433`
- Redis: `127.0.0.1:6379` — 08과 09-04에서만 사용
- Ollama 모델: `embeddinggemma`, `llama3.2`

공용 실행 환경은 상위 디렉터리의 `00_local-runtime`을 사용합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\00_local-runtime\scripts\start-local-services.ps1
docker exec aidevs-ollama ollama pull embeddinggemma
docker exec aidevs-ollama ollama pull llama3.2
python .\00_local-runtime\database\apply_schema.py
```

## 공용 파일

- `_pgvector_store.py`: Embedding, 저장, 유사도 검색
- `_ollama_rag.py`: 검색 결과로 Ollama 답변 생성
- `_redis_cache.py`: JSON 답변 Cache

Agent, MCP Tool, Metadata Filter, Hybrid Search는 기본 RAG 흐름을 이해한 다음 별도
예제에서 다룹니다.
