---
name: repo-analyzer
description: >
  Phân tích toàn bộ một code repository và tổng hợp thành 2 output đồng thời:
  landing page HTML tương tác và Markdown function docs.
  Trigger ngay khi người dùng đề cập: "phân tích repo", "đọc codebase", "tóm tắt project",
  "analyze repo", "summarize codebase", "hiểu repo này", hoặc cung cấp GitHub URL / local path
  và muốn hiểu nội dung. Luôn dùng skill này — đừng tự improvise workflow mà không đọc trước.
---

# Repo Analyzer Agent

Phân tích một repo (local hoặc GitHub) và tạo ra 2 output:
1. **`{repo_name}.html`** — landing page tương tác: architecture clickable, workflow tabs, function table, onboarding, requirements
2. **`functions.md`** — chi tiết từng function/class với signature + explanation

---

## Step 1 — Xác định input

Người dùng cung cấp một trong hai dạng:
- **Local path**: `/path/to/repo` hoặc `./my-project`
- **GitHub URL**: `https://github.com/owner/repo`

Nếu chưa rõ, hỏi ngay: *"Bạn muốn phân tích repo local hay GitHub URL?"*

---

## Step 2 — Ingestion

### Local repo (dùng `bash_tool`)

```bash
# File tree — lọc extensions quan trọng, loại trừ noise
find <path> -type f \
  \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" \
     -o -name "*.java" -o -name "*.rs" -o -name "*.rb" -o -name "*.jsx" \
     -o -name "*.tsx" -o -name "*.vue" -o -name "*.svelte" \
     -o -name "*.md" -o -name "*.json" -o -name "*.yaml" -o -name "*.toml" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" \
  ! -path "*/build/*" ! -path "*/__pycache__/*" ! -path "*/.venv/*" \
  | sort

# Tổng số dòng
find <path> -type f ... | xargs wc -l 2>/dev/null | tail -1

# Đếm usage của functions quan trọng
grep -r "function_name" . --include="*.py" | grep -v "^.*def function_name" | wc -l
```

**Thứ tự đọc file (priority order):**
1. README.md, README.rst
2. Package config: `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`
3. Entry points: `main.py`, `index.ts`, `app.js`, `cmd/`, `src/main.*`
4. Config: `.env.example`, `docker-compose.yml`, `Makefile`
5. Core modules (top-level src directories)

### GitHub URL (dùng `web_fetch` hoặc `git clone` qua `bash_tool`)

```bash
# Clone (nếu bash_tool khả dụng)
git clone --depth=1 https://github.com/owner/repo /tmp/repo-name

# Hoặc fetch qua GitHub API
# GET https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1
# GET https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{path}
```

**Với repo lớn (>100 files):** Chỉ đọc sâu top 30–40 file quan trọng nhất. Không cần đọc test files (chỉ scan tên).

---

## Step 3 — Analysis (trong context)

Phân tích tuần tự theo 4 chiều:

### 3a. Architecture
- Stack công nghệ (language, framework, DB, infra)
- Cấu trúc layer: vai trò từng folder/module chính
- Entry points và luồng khởi động
- External dependencies quan trọng
- Pattern kiến trúc (MVC, layered, microservices, event-driven…)

### 3b. Workflows chính
Xác định 2–4 workflows/flows chính. Mỗi workflow:
- Tên ngắn gọn (ví dụ: "Request lifecycle", "Authentication flow")
- Danh sách steps tuần tự, **mỗi step gắn với layer nào đang xử lý**
- Màu layer: blue=user/entry, green=public API, purple=domain/core, warn=utilities

### 3c. Functions/Classes inventory

Với mỗi function/class/method quan trọng:

| Field | Mô tả |
|---|---|
| `name` | Tên đầy đủ |
| `type` | `function` \| `class` \| `method` \| `hook` \| `middleware` |
| `file` | File path ngắn gọn |
| `signature` | Parameters + return type |
| `description` | 1–2 câu giải thích mục đích |
| `usage_count` | Số lần được gọi/import (ước tính qua grep) |
| `is_public` | `true` nếu exported/public |
| `is_entry_point` | `true` nếu là entry point |
| `has_side_effects` | `true` nếu có I/O, DB, network call |
| `importance_score` | 0–100, tính theo công thức bên dưới |

**Importance score formula:**
```
raw = (usage_count_normalized × 0.35)
    + (is_public × 0.25)
    + (is_entry_point × 0.25)
    + (has_side_effects × 0.15)

score = round(raw × 100)  # normalize về 0–100
```

Minimum 5 functions, tối đa 50. Sort by score descending.

### 3d. Onboarding highlights
- Quick start: **5 steps rõ ràng** theo thứ tự:
  1. Tạo và activate virtualenv (`python -m venv .venv` + lệnh activate theo OS)
  2. Install dependencies
  3. Setup config/env vars (nếu có)
  4. Bước chuẩn bị riêng của project (seed DB, build index, migrate, v.v. — nếu có)
  5. Chạy app
- 5–7 điểm cần biết ngay (cụ thể, actionable — không generic)
- "Start reading at": thứ tự đọc code cho người mới (step 1 → 2 → 3)

### 3e. Requirements
Chỉ liệt kê những gì cần thiết để chạy được project (không giải thích dài):
- Language version (e.g. `Python 3.10+`)
- Required packages/deps (từ `requirements.txt`, `package.json`, v.v.)
- Required env vars / credentials (nếu có)
- External services cần thiết (DB, API keys, v.v.)

---

## Step 4 — Tạo `{repo_name}.html` (Landing Page)

Đọc `references/landing-template.md` để lấy full HTML/CSS template.

**Cấu trúc 5 sections (collapsible `<details>`):**

| # | Section | Nội dung |
|---|---|---|
| 01 | Architecture | Interactive layer diagram (click → detail panel bên phải) |
| 02 | Workflow | Tab switcher, mỗi workflow là flow steps color-coded theo layer |
| 03 | Function importance | Styled table: name/type/file/badges/score bar |
| 04 | Onboarding quick start | 4 code steps + reading order + key points |
| 05 | Project requirements | 4-card grid: runtime, dev/build, compat, conventions |

**Quy tắc design bắt buộc:**
- Light theme, nền kem (#f5f4f0), card trắng
- 5 màu section riêng biệt: `--c1` blue · `--c2` teal · `--c3` violet · `--c4` amber · `--c5` rose
- Section titles: **IN HOA, bold (700), letter-spacing rộng**, border-left màu theo section
- Sub-titles bên trong diagram: **bold (700)**
- Fonts: IBM Plex Mono (mono) + Sora (sans)
- Không dùng KPI cards trên cùng
- Mỗi workflow step gắn màu layer tương ứng với architecture

Lưu tại: `./repo_docs/docs/{repo_name}/{repo_name}.html`

---

## Step 5 — Tạo `functions.md`

Đọc `references/functions-template.md` để lấy format chi tiết.

**Cấu trúc:**
- Header: repo name, date, tổng số functions
- Table of contents group theo file
- Mỗi function: heading + type badge + importance bar unicode + signature code block + description + used-in list
- Sort: entry points trước → sort by importance_score desc

Lưu tại: `./repo_docs/docs/{repo_name}/functions.md`

---

## Step 6 — Tạo / Update `CHANGELOG.md`

File này chỉ được **tạo một lần** (lần đầu), các lần sau **append thêm** — không bao giờ overwrite.

**Kiểm tra trước:**
```bash
# Kiểm tra CHANGELOG có tồn tại chưa
ls ./repo_docs/docs/{repo_name}/CHANGELOG.md
```

**Nếu chưa tồn tại (lần đầu tiên):** Tạo file với entry khởi tạo:
```markdown
# CHANGELOG — {repo_name}

## [init] {YYYY-MM-DD}

**Docs khởi tạo lần đầu.**

- Analyzed {N} files · {M} lines
- Stack: {primary stack}
- Tags: {2–5 tags ngắn gọn phân loại repo, ví dụ: AI, RAG, FastAPI, CLI, MCP, WebSocket, ML, Data, Infra}
- {N} functions/classes mapped
- Top functions: {top 3 function names}
```

**Cách chọn Tags:** ngắn, capitalized, dùng lại tag đã có nếu phù hợp. Ví dụ: `AI`, `RAG`, `MCP`, `Multi-Agent`, `FastAPI`, `CLI`, `LangChain`, `ChromaDB`, `FAISS`, `ML`, `Data`, `Infra`, `WebSocket`.

**Nếu đã tồn tại (lần update):** Đọc file, tìm entry `[update]` gần nhất:

- **Nếu entry `[update]` gần nhất có cùng ngày với lần chạy này**: thêm bullet vào entry đó, không tạo thêm
- **Nếu chưa có `[update]` nào, hoặc `[update]` gần nhất khác ngày**: tạo entry `[update]` mới lên đầu file (sau header `#`)
- **`[init]` không bao giờ bị sửa**, kể cả khi cùng ngày

```markdown
## [update] {YYYY-MM-DD}

**Thay đổi kể từ lần trước:**

- {file mới thêm vào}: mô tả ngắn thay đổi
- {file bị xóa}: removed
- {file thay đổi}: function X thêm/sửa/xóa
- Tổng: {+N functions added, -M removed, K modified}
```

Lưu tại: `./repo_docs/docs/{repo_name}/CHANGELOG.md`

---

## Step 7 — Present output

```
present_files([
  "./repo_docs/docs/{repo_name}/{repo_name}.html",
  "./repo_docs/docs/{repo_name}/functions.md",
  "./repo_docs/docs/{repo_name}/CHANGELOG.md"
])
```

Tóm tắt ngắn trong chat: repo là gì, stack gì, bao nhiêu functions, top 3 quan trọng nhất.

---

## Update mode

Khi người dùng nói *"update lại"*, *"repo có thay đổi"*, *"re-analyze"*:

1. **Đọc `CHANGELOG.md` hiện có** — biết docs đang ở trạng thái nào, lần phân tích trước có gì
2. Re-scan repo: lấy danh sách files hiện tại
3. So sánh với lần trước (dùng `find -newer` hoặc so sánh file list từ CHANGELOG)
4. Chỉ phân tích sâu các file thay đổi / mới
5. Regenerate HTML và Markdown
6. Append entry mới vào CHANGELOG (không overwrite)

---

## Edge cases

| Tình huống | Xử lý |
|---|---|
| Repo > 500 files | Chỉ đọc sâu top 40 files, ghi note trong output |
| File > 500 lines | Đọc 50 dòng đầu + 50 dòng cuối + grep functions |
| Private GitHub repo | Yêu cầu clone local hoặc provide token |
| Mono-repo | Hỏi: analyze toàn bộ hay sub-package cụ thể? |
| Non-code repo (chỉ docs) | Bỏ function inventory, focus vào document structure |
| GitHub API bị block | Dùng `git clone --depth=1` qua `bash_tool` thay thế |

---

## References

- `references/landing-template.md` — Full HTML/CSS/JS template cho index.html
- `references/functions-template.md` — Markdown template cho functions.md