# ARCHITECTURE — Repo Docs Hub

> Tài liệu kiến trúc hệ thống Repo Docs Hub.
> Cập nhật: 2026-04-20

---

## Mục tiêu

Xây dựng một **documentation hub tĩnh** có khả năng tự động đọc các repo con trong cùng thư mục, render landing page, và cung cấp viewer cho từng loại tài liệu — không cần build tool hay framework nặng.

---

## Cấu trúc thư mục

```
repo_docs/
├── ARCHITECTURE.md        ← tài liệu này
├── CHANGELOG.md           ← lịch sử thay đổi của chính hub
├── README.md              ← mô tả nhanh project
│
├── server.py              ← live-scan HTTP server (/repos.json động)
├── generate.py            ← script quét dirs → sinh repos.json (dùng độc lập)
├── start.sh               ← khởi động server.py
│
├── home.html              ← Landing page chính (auto-refresh 30s)
├── viewer.html            ← Universal viewer (HTML doc + Markdown)
├── repos.json             ← AUTO-GENERATED, gitignored
│
├── agent/                 ← AI agent phân tích repo tự động
│   ├── main.py            ← Entrypoint CLI (Strands Agent + OpenRouter)
│   ├── requirements.txt   ← strands, strands-tools, python-dotenv
│   ├── .env-template      ← template biến môi trường
│   └── skills/
│       └── repo-analyzer/ ← Skill: sinh landing page HTML + functions.md
│           ├── SKILL.md   ← Skill definition & instructions
│           └── references/
│               ├── landing-template.md   ← Template HTML output
│               └── functions-template.md ← Template Markdown output
│
└── docs/                  ← Tất cả repo con đặt ở đây
    └── [repo-name]/
        ├── CHANGELOG.md   ← lịch sử repo con (bắt buộc)
        ├── functions.md   ← function reference (bắt buộc)
        └── [repo-name].html  ← HTML knowledge doc (bắt buộc)
```

---

## Luồng dữ liệu

```
start.sh
  └─► server.py (ThreadingHTTPServer)
        ├── GET /repos.json → scan_repos() ngay lúc request
        │     ├── Quét tất cả thư mục con trong repo_docs/docs/
        │     ├── Đọc CHANGELOG.md → parse entries (tag, date, note, details)
        │     ├── Extract: stack, stats (files/lines/functions), description
        │     └── Trả JSON trực tiếp (không ghi file)
        └── GET /* → serve static files bình thường

home.html (load trong browser)
  ├── boot() → fetch("repos.json") → render grid
  ├── Auto-refresh: setInterval 30s → boot() lại (silent)
  ├── Countdown hiển thị trên nút "↺ Reload repos · Xs"
  └── Render grid các repo cards
              ├── Click card → expand → 3 buttons
              │     ├── [Changelog]  → modal overlay (data từ repos.json)
              │     ├── [HTML Doc]   → navigate viewer.html?type=html&...
              │     └── [Functions]  → navigate viewer.html?type=functions&...
              └── Badge: latest date lấy từ changelog[0].date

viewer.html (nhận URL params)
  ├── ?type=html&file=...&title=...
  │     └── Render iframe toàn màn hình + top bar với back button
  └── ?type=functions&file=...&title=...
        └── fetch(file) → marked.parse() → render markdown styled
```

---

## Các thành phần

### `server.py`
- Kế thừa `SimpleHTTPRequestHandler` + `ThreadingHTTPServer`
- Override `do_GET`: nếu path là `/repos.json` → gọi `scan_repos()` trực tiếp, trả JSON với header `Cache-Control: no-store`
- Các path khác → delegate lên `super().do_GET()` (serve static)
- Không ghi `repos.json` ra disk — mỗi request là một lần scan mới

### `generate.py`
- **Input:** toàn bộ subdirectory trong `repo_docs/docs/`
- **Output:** `repos.json` — array các repo object (dùng khi cần file tĩnh)
- **Logic:**
  - Bỏ qua thư mục ẩn (`.xxx`) và thư mục không có doc file nào
  - Parse `CHANGELOG.md` bằng regex:
    - Header: `## [tag] YYYY-MM-DD`
    - Note: dòng **bold** đầu tiên
    - Details: các bullet point (`- ...`)
  - Extract từ entry `[init]`: stack, files/lines/functions stats, description
  - Fallback description: từ `<title>` của HTML file

### `home.html`
- Không hardcode data — luôn fetch `repos.json` khi load
- Render card grid với CSS Grid (auto-fill, minmax 300px)
- Card state machine: `default` → `expanded` (click) → `default` (click lại)
- Modal changelog: render danh sách entries có tag + date + note + details
- Navigate sang viewer: truyền `file`, `type`, `title` qua URL search params

### `viewer.html`
- Đọc URL params: `file`, `type`, `title`
- Top bar cố định: back button (`history.back()`) + tên file + loại doc
- `type=html`: `<iframe>` fill toàn bộ viewport bên dưới top bar
- `type=functions`: fetch file → `marked.parse()` → render với custom CSS

### `start.sh`
```
[1] python3 server.py [port]
    → live-scan HTTP server tại http://localhost:8080/home.html
    → /repos.json được scan động, không cần restart khi thêm repo
```

### `agent/main.py`
- CLI nhận `repo_path` + `--name` (optional)
- Load `.env` từ cùng thư mục → đọc `OPENROUTER_API_KEY`
- Khởi tạo `OpenAIModel` trỏ tới OpenRouter (model: `anthropic/claude-haiku-4-5`)
- Tạo `Agent` với tools: `shell`, `file_write`, `editor` + plugin `AgentSkills` load từ `skills/`
- System prompt yêu cầu exclude `.venv`, `node_modules`, `__pycache__`, `.git` khi scan
- Gọi `agent("Phân tích repo tại: {path}, tên: {name}")` → skill tự xử lý toàn bộ

### `agent/skills/repo-analyzer/`
- Skill definition trong `SKILL.md`: instructions cho agent cách sinh output
- `references/landing-template.md`: HTML template cho landing page repo
- `references/functions-template.md`: Markdown template cho function reference
- Output: tạo `docs/[repo-name]/` với 3 files bắt buộc

---

## Quy ước repo con

Mỗi thư mục con được nhận dạng là **repo hợp lệ** nếu có ít nhất 1 trong:
- `CHANGELOG.md`
- `functions.md`
- `*.html`

### Format CHANGELOG.md (bắt buộc để parse đúng)

```markdown
# CHANGELOG — [repo-name]

## [update] YYYY-MM-DD

**Mô tả ngắn thay đổi.**

- bullet point 1
- bullet point 2

---

## [init] YYYY-MM-DD

**Docs khởi tạo lần đầu.**

- Analyzed N files · M lines
- Stack: Tech1, Tech2, Tech3
- N functions/classes mapped
- Top functions: `fn1`, `fn2`
```

**Các tag hỗ trợ:** `init` · `update` · `fix` · `refactor` · `breaking`

---

## Mở rộng

**Thêm repo thủ công:**
1. Tạo thư mục `repo_docs/docs/[repo-name]/`
2. Đặt vào đó: `CHANGELOG.md`, `functions.md`, `[repo-name].html`
3. Chạy lại `start.sh` — hub tự cập nhật, không cần sửa code

**Thêm repo bằng agent:**
```bash
cd agent && python main.py /path/to/repo
```
Agent tự sinh đủ 3 files vào `docs/[repo-name]/`.

---

## Phụ thuộc

| Thành phần | Phụ thuộc |
|---|---|
| `server.py` | Python 3.x stdlib (http.server, json, urllib) |
| `generate.py` | Python 3.x stdlib (os, json, re, glob) |
| `home.html` | marked.js (CDN), Google Fonts (CDN) |
| `viewer.html` | marked.js (CDN), Google Fonts (CDN) |
| `start.sh` | Python 3.x, bash |
| `agent/main.py` | strands, strands-tools, python-dotenv, OPENROUTER_API_KEY |

Hub chạy không cần npm, không có build step, không có framework.
Agent cần `pip install -r agent/requirements.txt` và file `agent/.env`.
