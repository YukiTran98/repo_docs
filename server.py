#!/usr/bin/env python3
"""
server.py — HTTP server với live-scan endpoint.

Khác với 'python -m http.server' thông thường:
- GET /repos.json  → scan docs/ ngay lúc request, trả JSON mới nhất
- Các file khác    → serve static như bình thường

Thêm repo mới vào docs/ → refresh browser là xong, không cần restart.
"""

import http.server
import json
import os
import subprocess
import sys
import threading
import urllib.parse
import uuid

from generate import scan_repos

BASE = os.path.dirname(os.path.abspath(__file__))
AGENT_MAIN = os.path.join(BASE, 'agent', 'main.py')
VENV_PYTHON = os.path.join(BASE, '.venv', 'bin', 'python')

# job_id -> {status, log, returncode}
JOBS = {}
JOBS_LOCK = threading.Lock()


def _run_agent(job_id: str, repo_path: str, repo_name: str):
    with JOBS_LOCK:
        JOBS[job_id] = {'status': 'running', 'log': '', 'returncode': None}

    python = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable
    cmd = [python, AGENT_MAIN, repo_path, '--name', repo_name]

    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, cwd=BASE
    )
    log = []
    for line in proc.stdout:
        log.append(line)
        with JOBS_LOCK:
            JOBS[job_id]['log'] = ''.join(log)
    proc.wait()

    with JOBS_LOCK:
        JOBS[job_id]['status'] = 'done' if proc.returncode == 0 else 'error'
        JOBS[job_id]['returncode'] = proc.returncode


class LiveScanHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path

        if path == '/repos.json':
            self._serve_repos_json()
        elif path.startswith('/analyze/status/'):
            job_id = path.split('/')[-1]
            self._serve_job_status(job_id)
        else:
            super().do_GET()

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        if path == '/analyze':
            self._handle_analyze()
        else:
            self.send_response(404)
            self.end_headers()

    def _handle_analyze(self):
        length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(length))
        repo_path = body.get('repo_path', '').strip()
        repo_name = body.get('repo_name', '').strip() or os.path.basename(repo_path)

        if not repo_path or not os.path.isdir(repo_path):
            self._json(400, {'error': f'Không tìm thấy thư mục: {repo_path}'})
            return

        job_id = str(uuid.uuid4())[:8]
        t = threading.Thread(target=_run_agent, args=(job_id, repo_path, repo_name), daemon=True)
        t.start()
        self._json(200, {'job_id': job_id})

    def _serve_job_status(self, job_id: str):
        with JOBS_LOCK:
            job = JOBS.get(job_id)
        if not job:
            self._json(404, {'error': 'Job not found'})
            return
        self._json(200, job)

    def _json(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_repos_json(self):
        try:
            repos = scan_repos()
            body = json.dumps(repos, ensure_ascii=False, indent=2).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            self.wfile.write(body)
            print(f'  ↺  /repos.json  →  {len(repos)} repo(s) scanned')
        except Exception as e:
            error = json.dumps({'error': str(e)}).encode('utf-8')
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(error)))
            self.end_headers()
            self.wfile.write(error)

    def log_message(self, fmt, *args):
        # Bỏ log /repos.json (đã in riêng ở trên), giữ lại request khác
        if args and '/repos.json' in str(args[0]):
            return
        super().log_message(fmt, *args)


def main(port: int = 8080):
    os.chdir(BASE)
    addr = ('', port)

    # ThreadingHTTPServer để không block khi scan
    with http.server.ThreadingHTTPServer(addr, LiveScanHandler) as httpd:
        print()
        print('  Repo Docs Hub — live scan mode')
        print('  ─────────────────────────────────────')
        print(f'  → http://localhost:{port}/home.html')
        print()
        print('  Thêm repo mới vào docs/ → F5 là xong.')
        print('  Ctrl+C để dừng.')
        print('  ─────────────────────────────────────')
        print()
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print('\n  Server stopped.')


if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    main(port)
