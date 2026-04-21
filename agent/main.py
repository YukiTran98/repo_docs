#!/usr/bin/env python3
"""
Usage:
    python main.py /path/to/repo
    python main.py /path/to/repo --name custom-name
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from strands import Agent
from strands.models.openai import OpenAIModel
from strands.vended_plugins.skills import AgentSkills
from strands_tools import shell, file_write, editor

SKILLS_DIR = Path(__file__).parent / "skills"
AGENT_DIR = Path(__file__).parent


def build_model():
    if key := os.environ.get("ANTHROPIC_API_KEY"):
        from strands.models.anthropic import AnthropicModel
        print("[provider] Anthropic")
        return AnthropicModel(
            model_id="claude-haiku-4-5-20251001",
            params={"max_tokens": 16000},
        )

    if key := os.environ.get("OPENAI_API_KEY"):
        print("[provider] OpenAI")
        return OpenAIModel(
            client_args={"api_key": key},
            model_id="gpt-4o-mini",
            params={"max_tokens": 16000},
        )

    if key := os.environ.get("GOOGLE_API_KEY"):
        print("[provider] Google Gemini")
        return OpenAIModel(
            client_args={
                "api_key": key,
                "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
            },
            model_id="gemini-2.0-flash",
            params={"max_tokens": 16000},
        )

    if key := os.environ.get("OPENROUTER_API_KEY"):
        print("[provider] OpenRouter")
        return OpenAIModel(
            client_args={
                "api_key": key,
                "base_url": "https://openrouter.ai/api/v1",
            },
            model_id="anthropic/claude-haiku-4-5",
            params={"max_tokens": 16000},
        )

    print("[ERROR] Không tìm thấy API key nào. Cần ít nhất một trong: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, OPENROUTER_API_KEY")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_path", help="Đường dẫn tới repo cần phân tích")
    parser.add_argument("--name", help="Tên output (mặc định: tên thư mục repo)")
    args = parser.parse_args()

    repo_path = Path(args.repo_path).resolve()
    if not repo_path.is_dir():
        print(f"[ERROR] Không tìm thấy: {repo_path}")
        sys.exit(1)

    repo_name = args.name or repo_path.name
    out_dir = str(AGENT_DIR.parent / "docs" / repo_name)

    agent = Agent(
        model=build_model(),
        tools=[shell, file_write, editor],
        plugins=[AgentSkills(skills=[str(SKILLS_DIR)])],
        system_prompt=(
            "Khi scan files, LUÔN exclude: .venv, venv, node_modules, __pycache__, .git, dist, build. "
            "Dùng find với: ! -path '*/.venv/*' ! -path '*/node_modules/*' ! -path '*/__pycache__/*' ! -path '*/.git/*'. "
            "Khi ghi HTML hoặc file lớn, chia thành nhiều lần ghi nếu cần — đừng để bị truncate. "
            "Output dir tuyệt đối đã được cung cấp trong task — dùng đúng path đó, không tự tính theo ./repo_docs/docs/."
        ),
    )

    agent(f"Phân tích repo tại: {repo_path}, tên: {repo_name}. Lưu tất cả output vào thư mục: {out_dir}/")


if __name__ == "__main__":
    main()
