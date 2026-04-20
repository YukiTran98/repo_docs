# CHANGELOG — repo_docs hub

## [update] 2026-04-12

**Thêm live-scan server và auto-refresh.**

- Thêm server.py — custom HTTP server, /repos.json được scan động mỗi request
- start.sh đơn giản hóa: chỉ gọi server.py (bỏ bước generate.py riêng)
- home.html: thêm nút "Reload repos" + auto-refresh countdown 30s
- Thêm repo mới vào docs/ → F5 hoặc chờ 30s là thấy, không cần restart server

---

## [update] 2026-04-12

**Refactor sang kiến trúc auto-discovery.**

- Thay index.html bằng home.html — fetch repos.json thay vì hardcode
- Thêm viewer.html — universal viewer cho HTML doc và functions.md
- Thêm generate.py — auto-scan subdirs, parse CHANGELOG, sinh repos.json
- Thêm start.sh — one-command start: generate + serve
- Thêm ARCHITECTURE.md mô tả kiến trúc hệ thống
- Thêm README.md và CHANGELOG.md cho hub

---

## [init] 2026-04-12

**Khởi tạo Repo Docs Hub lần đầu.**

- Analyzed repo_docs structure
- Stack: HTML, CSS, JavaScript, Python, marked.js
- Landing page tĩnh với hardcoded repo data
- Hỗ trợ: card grid, changelog strip, modal functions.md viewer
