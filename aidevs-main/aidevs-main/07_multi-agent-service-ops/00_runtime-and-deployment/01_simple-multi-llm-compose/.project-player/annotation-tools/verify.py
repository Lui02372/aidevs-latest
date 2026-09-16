# 읽기 전용 검증: 앱/초기화 모듈 import, 서버/DB 조작, .env 접근 없이 실행한다.
from pathlib import Path
import ast
import datetime
import difflib
import hashlib
import importlib.util
import io
import json
import re
import sys
import tokenize

sys.stdout.reconfigure(encoding='utf-8')
ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT/'.project-player/annotation-baseline'
manifest = json.loads((BASE/'manifest.json').read_text(encoding='utf-8'))
expected = json.loads((ROOT/'.project-player/annotation-tools/annotation-result.json').read_text(encoding='utf-8'))
results = {}
all_pass = True
for name, meta in manifest['files'].items():
    old = (BASE/name).read_bytes()
    new = (ROOT/name).read_bytes()
    checks = {'baseline_sha256':hashlib.sha256(old).hexdigest()==meta['sha256']}
    if name in expected['files']:
        checks['no_external_changes']=hashlib.sha256(new).hexdigest()==expected['files'][name]['sha256']
    else:
        checks['unmodified']=old==new
    added = []
    for tag,a,b,c,d in difflib.SequenceMatcher(None,old.splitlines(keepends=True),new.splitlines(keepends=True),autojunk=False).get_opcodes():
        if tag == 'equal': continue
        checks['insert_only'] = checks.get('insert_only',True) and tag=='insert'
        added.extend(new.splitlines(keepends=True)[c:d])
    checks['only_learning_comments']=all(row.lstrip().startswith(('# [학습]'.encode(),'-- [학습]'.encode())) for row in added)
    checks['encoding_line_endings_preserved']=new.count(b'\r\n')==old.count(b'\r\n') and all(row.endswith(b'\n') and not row.endswith(b'\r\n') for row in added)
    if name.endswith('.py'):
        trees = [ast.parse(b,filename=name,feature_version=(3,12)) for b in [old,new]]
        checks['python_312_grammar_before_after']=True
        checks['ast_equal_without_locations']=ast.dump(trees[0],include_attributes=False)==ast.dump(trees[1],include_attributes=False)
        def meaningful_tokens(data):
            return [(t.type,t.string) for t in tokenize.tokenize(io.BytesIO(data).readline) if t.type not in (tokenize.COMMENT,tokenize.NL,tokenize.ENCODING)]
        checks['python_tokens_equal']=meaningful_tokens(old)==meaningful_tokens(new)
    if name.endswith('.sql'):
        import sqlparse
        def sql_tokens(data):
            return [(str(t.ttype),t.value) for stmt in sqlparse.parse(data.decode('utf-8')) for t in stmt.flatten() if not t.is_whitespace and t.ttype not in sqlparse.tokens.Comment]
        checks['sql_tokens_equal_not_grammar_validation']=sql_tokens(old)==sql_tokens(new)
    if name.endswith('requirements.txt'):
        def requirements(data):
            return [s for s in data.decode('utf-8').splitlines() if s.strip() and not s.lstrip().startswith('#')]
        checks['requirements_lines_equal_not_parser_validation']=requirements(old)==requirements(new)
    all_pass = all_pass and all(checks.values())
    results[name]={'checks':checks,'added_lines':len(added),'final_lines':len(new.splitlines()),'sha256':hashlib.sha256(new).hexdigest()}

document = ROOT/'docs/project-walkthrough.md'
doc_checks = {}
if document.exists():
    text = document.read_text(encoding='utf-8')
    doc_checks['ten_sections'] = len(re.findall(r'^## (?:[1-9]|10)\.',text,re.M))==10
    diagrams = re.findall(r'```mermaid\n(.*?)```',text,re.S)
    doc_checks['two_diagrams'] = len(diagrams)==2 and diagrams[0].startswith('flowchart TD\n') and diagrams[1].startswith('sequenceDiagram\n')
    references=[]
    for path,number in re.findall(r'\]\(\.\./([^\)#]+)#L(\d+)\)',text):
        p=ROOT/path
        references.append(p.is_file() and 1<=int(number)<=len(p.read_bytes().splitlines()))
    doc_checks['reference_paths_and_line_bounds']=bool(references) and all(references)
    anchors=json.loads((ROOT/'.project-player/annotation-tools/document-anchors.json').read_text(encoding='utf-8'))
    doc_checks['all_reference_symbols_match_final_lines']=all(a['needle'] in (ROOT/a['path']).read_text(encoding='utf-8').splitlines()[a['line']-1] for a in anchors)
    # 전문 Mermaid 파서 대신 제한된 연결·블록 구조만 검사한다.
    ids=set(re.findall(r'^    ([A-Za-z][A-Za-z0-9]*)\[',diagrams[0],re.M))
    edges=re.findall(r'^    ([A-Za-z][A-Za-z0-9]*) -->.*? ([A-Za-z][A-Za-z0-9]*)$',diagrams[0],re.M)
    actors=set(re.findall(r'^    (?:actor|participant) ([A-Za-z][A-Za-z0-9]*) as',diagrams[1],re.M))
    messages=re.findall(r'^\s+([A-Za-z][A-Za-z0-9]*)(?:->>|-->>)([A-Za-z][A-Za-z0-9]*):',diagrams[1],re.M)
    doc_checks['mermaid_ids_only_not_parser']=all(a in ids and b in ids for a,b in edges) and all(a in actors and b in actors for a,b in messages)
    doc_checks['mermaid_alt_balance_only']=len(re.findall(r'^\s+alt ',diagrams[1],re.M))==len(re.findall(r'^\s+end$',diagrams[1],re.M))
    doc_checks['annotation_rerun_added_nothing']=all(r['status']=='already_annotated' for r in expected['files'].values())
    doc_checks['all_source_files_named']=all(name in text for name in manifest['files'])
    doc_checks['no_template_tokens']='[[' not in text and 'TODO' not in text
    new_content = text+'\n'+'\n'.join(row.decode('utf-8') for name in expected['files'] for row in (ROOT/name).read_bytes().splitlines() if '[학습]'.encode() in row)
    doc_checks['no_secret_patterns_in_new_content']=not re.search(r'sk-[A-Za-z0-9_-]{16,}|AIza[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,}|-----BEGIN .*PRIVATE KEY|postgresql://[^\s]+:[^\s]+@',new_content)
    all_pass = all_pass and all(doc_checks.values())
report={'checked_at':datetime.datetime.now().astimezone().isoformat(),'python':sys.version.split()[0],'overall_static_pass':all_pass,'files':results,'document':doc_checks,'reference_count':len(references) if document.exists() else 0,'limitations':['No YAML/Compose parser','No Dockerfile parser','No packaging requirements parser','sqlparse is not a PostgreSQL grammar validator','No Mermaid renderer/parser','No pytest/FastAPI/Streamlit in this validation interpreter']}
(ROOT/'.project-player/annotation-tools/verification-result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if all_pass else 1)
