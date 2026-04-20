#!/usr/bin/env python3
"""
generate.py — Quét toàn bộ thư mục con trong repo_docs/docs/,
               parse docs, và sinh ra repos.json cho home.html.

Chạy trực tiếp:
    python3 generate.py

Hoặc qua start.sh (tự động chạy trước khi khởi server).
"""

import os
import json
import re
import glob

# BASE: thư mục chứa generate.py (tức repo_docs/)
BASE = os.path.dirname(os.path.abspath(__file__))
# DOCS_DIR: thư mục chứa tất cả repo con
DOCS_DIR = os.path.join(BASE, 'docs')

# Thư mục / tiền tố bị bỏ qua khi quét
IGNORE_DIRS = {'.', '..'}
IGNORE_PREFIXES = ('.', '_')


# ──────────────────────────────────────────
# CHANGELOG PARSER
# ──────────────────────────────────────────

def parse_changelog(path: str) -> list[dict]:
    """Parse CHANGELOG.md → list of entry dicts."""
    with open(path, encoding='utf-8') as f:
        content = f.read()

    entries = []
    # Tách theo dải phân cách ---
    blocks = re.split(r'\n---\n', content)

    for block in blocks:
        m = re.search(r'##\s+\[(\w+)\]\s+(\d{4}-\d{2}-\d{2})', block)
        if not m:
            continue

        tag = m.group(1).lower()
        date = m.group(2)

        # Dòng bold đầu tiên làm note
        bold_m = re.search(r'\*\*(.+?)\*\*', block)
        note = bold_m.group(1).strip() if bold_m else ''

        # Bullet points làm details
        details = re.findall(r'^\s*-\s+(.+)', block, re.MULTILINE)

        entries.append({
            'tag': tag,
            'date': date,
            'note': note,
            'details': [d.strip() for d in details],
        })

    return entries


def extract_meta(changelog: list[dict]) -> tuple[list, list, dict, str]:
    """
    Trích xuất stack, tags, stats, description từ entry [init].
    Trả về: (stack, tags, stats, description)
    """
    stack = []
    tags = []
    stats = {'files': 0, 'lines': 0, 'functions': 0}
    description = ''

    for entry in changelog:
        if entry['tag'] != 'init':
            continue

        description = entry.get('note', '')

        for detail in entry.get('details', []):
            # Stack: Python, openai-agents, ChromaDB, ...
            stack_m = re.search(r'Stack:\s*(.+)', detail, re.IGNORECASE)
            if stack_m:
                raw = stack_m.group(1)
                raw = re.sub(r'\(.*?\)', '', raw)
                stack = [s.strip() for s in raw.split(',') if s.strip()]

            # Tags: AI, Multi-Agent, MCP, ...
            tags_m = re.search(r'Tags:\s*(.+)', detail, re.IGNORECASE)
            if tags_m:
                tags = [t.strip() for t in tags_m.group(1).split(',') if t.strip()]

            # Analyzed N files · M lines
            files_m = re.search(
                r'Analyzed\s+(\d+)\s+files?\s*[·•]\s*(\d+)\s+lines?',
                detail, re.IGNORECASE
            )
            if files_m:
                stats['files'] = int(files_m.group(1))
                stats['lines'] = int(files_m.group(2))

            # N functions/classes mapped
            fn_m = re.search(r'(\d+)\s+functions?', detail, re.IGNORECASE)
            if fn_m:
                stats['functions'] = int(fn_m.group(1))

        break  # Chỉ lấy entry init đầu tiên

    return stack, tags, stats, description


def fallback_description(html_path: str) -> str:
    """Lấy description từ <title> của HTML file nếu không có từ changelog."""
    try:
        with open(html_path, encoding='utf-8') as f:
            head = f.read(3000)
        m = re.search(r'<title>(.+?)</title>', head, re.IGNORECASE)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    return ''


# ──────────────────────────────────────────
# SCANNER
# ──────────────────────────────────────────

def scan_repos() -> list[dict]:
    repos = []

    if not os.path.isdir(DOCS_DIR):
        return repos

    entries = sorted(os.listdir(DOCS_DIR))
    for entry in entries:
        # Bỏ qua file và thư mục đặc biệt
        if any(entry.startswith(p) for p in IGNORE_PREFIXES):
            continue
        path = os.path.join(DOCS_DIR, entry)
        if not os.path.isdir(path):
            continue

        changelog_path = os.path.join(path, 'CHANGELOG.md')
        functions_path = os.path.join(path, 'functions.md')
        html_files = sorted(glob.glob(os.path.join(path, '*.html')))

        # Phải có ít nhất 1 loại doc file
        has_changelog = os.path.exists(changelog_path)
        has_functions = os.path.exists(functions_path)
        has_html = bool(html_files)

        if not (has_changelog or has_functions or has_html):
            continue

        # Parse changelog
        changelog = parse_changelog(changelog_path) if has_changelog else []
        stack, tags, stats, description = extract_meta(changelog)

        # Fallback description từ HTML title
        if not description and has_html:
            description = fallback_description(html_files[0])

        # Paths tương đối từ BASE (repo_docs/)
        html_rel = os.path.relpath(html_files[0], BASE).replace('\\', '/') if has_html else None
        functions_rel = f'docs/{entry}/functions.md' if has_functions else None
        changelog_rel = f'docs/{entry}/CHANGELOG.md' if has_changelog else None

        repos.append({
            'id': entry,
            'name': entry,
            'description': description,
            'stack': stack,
            'tags': tags,
            'stats': stats,
            'htmlFile': html_rel,
            'functionsFile': functions_rel,
            'changelogFile': changelog_rel,
            'changelog': changelog,
        })

    return repos


# ──────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────

def main():
    print('🔍 Scanning repo_docs/docs/...')
    repos = scan_repos()

    output = os.path.join(BASE, 'repos.json')
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(repos, f, indent=2, ensure_ascii=False)

    print(f'✓ repos.json generated — {len(repos)} repo(s) found\n')
    for r in repos:
        fn_count = r['stats']['functions']
        cl_count = len(r['changelog'])
        latest = r['changelog'][0]['date'] if r['changelog'] else '—'
        print(f"  · {r['name']:<30} {fn_count} fn · {cl_count} changelog entries · latest {latest}")

    if not repos:
        print('  (no repos found — check that subdirectories have CHANGELOG.md / functions.md / *.html)')


if __name__ == '__main__':
    main()
