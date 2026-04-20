# Repo Docs Hub

Documentation hub cho tất cả repositories trong workspace `loitv2/data_science`.
Tự động đọc các thư mục con, parse changelog, và render landing page tương tác.

## Cấu trúc

```
repo_docs/
├── home.html          ← Landing page (auto-refresh 30s)
├── viewer.html        ← Viewer cho HTML doc & functions.md
├── server.py          ← Live-scan HTTP server
├── generate.py        ← Quét dirs → sinh repos.json (standalone)
├── start.sh           ← Khởi động server.py
├── repos.json         ← Auto-generated, không commit (gitignored)
├── ARCHITECTURE.md    ← Kiến trúc hệ thống
├── agent/             ← AI agent tự động phân tích repo
│   ├── main.py        ← Entrypoint (Strands + OpenRouter)
│   ├── .env-template  ← Template biến môi trường
│   └── skills/
│       └── repo-analyzer/  ← Skill sinh landing page + functions.md
└── docs/              ← Tất cả repo con đặt ở đây
    └── [repo-name]/
        ├── CHANGELOG.md
        ├── functions.md
        └── [repo-name].html
```

## Khởi động nhanh

```bash
cd repo_docs
./start.sh
# → http://localhost:8080/home.html
```

Port tùy chọn:
```bash
./start.sh 3000
```

## Thêm repo mới

1. Tạo thư mục `repo_docs/docs/[repo-name]/`
2. Đặt vào: `CHANGELOG.md`, `functions.md`, `[repo-name].html`
3. **Không cần restart** — trang tự reload sau tối đa 30s, hoặc bấm "↺ Reload repos"

Format CHANGELOG.md phải theo chuẩn (xem [ARCHITECTURE.md](ARCHITECTURE.md)).

## Dùng agent phân tích repo tự động

```bash
cd agent
cp .env-template .env
# Điền OPENROUTER_API_KEY vào .env

pip install -r requirements.txt
python main.py /path/to/repo
# → sinh docs/[repo-name]/ với CHANGELOG.md, functions.md, [repo].html
```

## Phụ thuộc

**Hub (server + viewer):**
- Python 3.x (stdlib only — không cần pip install)
- Browser hiện đại (Chrome / Firefox / Edge)
- Kết nối internet lần đầu (load Google Fonts + marked.js CDN)

**Agent:**
- Python 3.x + `pip install -r agent/requirements.txt`
- `OPENROUTER_API_KEY` (xem `agent/.env-template`)
