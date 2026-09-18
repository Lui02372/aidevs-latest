"""Start 05 locally, check HTTP + real MCP handshake, then stop only these processes.

Run with .venvs/weather/Scripts/python.exe. No API keys, Docker or cloud calls.
This checks startup/connectivity, not rendered UI behavior or weather generation.
"""
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
from urllib.error import URLError
from urllib.request import urlopen

PROJECT = Path(__file__).resolve().parent / '05_weather-mcp-deployment-project'


def allocate_ports():
    sockets = []
    try:
        for _ in range(3):
            sock = socket.socket()
            sock.bind(('127.0.0.1', 0))
            sockets.append(sock)
        return [sock.getsockname()[1] for sock in sockets]
    finally:
        for sock in sockets:
            sock.close()


def wait_http(url, process):
    deadline = time.monotonic() + 60
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f'Process exited with {process.returncode}: {url}')
        try:
            with urlopen(url, timeout=3) as response:
                return response.read()
        except (URLError, TimeoutError, ConnectionError):
            time.sleep(0.5)
    raise TimeoutError(url)


def main():
    mcp_port, backend_port, frontend_port = allocate_ports()
    children = []
    with tempfile.TemporaryDirectory(prefix='runtime-smoke-') as temp:
        handles = []
        try:
            def start(name, arguments, directory, extra_env=None):
                logfile = open(Path(temp) / f'{name}.log', 'w', encoding='utf-8')
                handles.append(logfile)
                env = os.environ.copy()
                env.update(extra_env or {})
                env['PYTHONUNBUFFERED'] = '1'
                process = subprocess.Popen(
                    [sys.executable, *arguments], cwd=directory, env=env,
                    stdout=logfile, stderr=subprocess.STDOUT,
                    creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
                )
                children.append(process)
                return process

            mcp = start('mcp', ['-m', 'uvicorn', 'server:mcp.streamable_http_app',
                                '--factory', '--host', '127.0.0.1', '--port', str(mcp_port)],
                        PROJECT / 'mcp_server')
            wait_http(f'http://127.0.0.1:{mcp_port}/health', mcp)
            backend = start('backend', ['-m', 'uvicorn', 'app:app', '--host', '127.0.0.1',
                                        '--port', str(backend_port)], PROJECT / 'backend',
                            {'WEATHER_MCP_URL': f'http://127.0.0.1:{mcp_port}/mcp'})
            ready = json.loads(wait_http(f'http://127.0.0.1:{backend_port}/health/ready', backend))
            assert ready['status'] == 'ok' and 'get_weather' in ready['tools'], ready
            frontend = start('frontend', ['-m', 'streamlit', 'run', 'app.py',
                                          '--server.headless=true', '--server.address=127.0.0.1',
                                          f'--server.port={frontend_port}',
                                          '--browser.gatherUsageStats=false'], PROJECT / 'frontend',
                             {'BACKEND_URL': f'http://127.0.0.1:{backend_port}'})
            assert wait_http(f'http://127.0.0.1:{frontend_port}/_stcore/health', frontend) == b'ok'
        except Exception:
            for handle in handles:
                handle.flush()
            for path in Path(temp).glob('*.log'):
                print(f'--- {path.name} ---\n{path.read_text(encoding="utf-8", errors="replace")[-4000:]}')
            raise
        finally:
            for process in reversed(children):
                if process.poll() is None:
                    if os.name == 'nt':
                        # A Windows venv python.exe can redirect to a child interpreter.
                        # Stop that tree while its parent is still alive.
                        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'],
                                       check=True, capture_output=True,
                                       creationflags=subprocess.CREATE_NO_WINDOW)
                    else:
                        process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=10)
            for handle in handles:
                handle.close()
    print('PASS: MCP health, backend MCP tools/list handshake, Streamlit server health; processes stopped')


if __name__ == '__main__':
    main()
