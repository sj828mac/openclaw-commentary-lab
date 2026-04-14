#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
SOURCE_CASE = WORKSPACE / "openclaw-commentary-mvp" / "cases" / "ai-hedge-fund"
POSTS_DIR = ROOT / "posts"
CONTENT_DIR = ROOT / "content"


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    html: list[str] = []
    in_list = False
    for raw in lines:
        line = raw.rstrip()
        if not line:
            if in_list:
                html.append("</ul>")
                in_list = False
            continue
        if line.startswith("# "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("## "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("> "):
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<blockquote>{line[2:]}</blockquote>")
        elif line.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"<li>{line[2:]}</li>")
        else:
            if in_list:
                html.append("</ul>")
                in_list = False
            html.append(f"<p>{line}</p>")
    if in_list:
        html.append("</ul>")
    return "\n".join(html)


def wrap_page(title: str, style: str, description: str, content_html: str) -> str:
    template = (ROOT / "templates" / "post-template.html").read_text(encoding="utf-8")
    return (
        template.replace("{{TITLE}}", title)
        .replace("{{STYLE}}", style)
        .replace("{{DESCRIPTION}}", description)
        .replace("{{CONTENT}}", content_html)
    )


def write_post(md_name: str, out_name: str, title: str, style: str, description: str) -> dict:
    md = (SOURCE_CASE / md_name).read_text(encoding="utf-8")
    html = wrap_page(title, style, description, md_to_html(md))
    out_path = POSTS_DIR / out_name
    out_path.write_text(html, encoding="utf-8")
    return {
        "slug": out_name.removesuffix(".html"),
        "title": title,
        "style": style,
        "description": description,
        "topic": "ai-hedge-fund",
        "status": "published",
        "path": f"posts/{out_name}",
    }


def main() -> int:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    posts = [
        write_post(
            "publish-ready-v1.md",
            "ai-hedge-fund-editorial.html",
            "ai-hedge-fund 長文評論版",
            "Editorial",
            "完整論述版，適合正式 blog / 電子報。",
        ),
        write_post(
            "short-post-v1.md",
            "ai-hedge-fund-quick.html",
            "ai-hedge-fund 短版快評版",
            "Quick Take",
            "縮短版核心觀點，適合快速發佈。",
        ),
        write_post(
            "channel-variants.md",
            "ai-hedge-fund-channel.html",
            "ai-hedge-fund 渠道變體版",
            "Channel Variants",
            "Telegram / Threads / Blog intro 三種渠道輸出。",
        ),
    ]
    (CONTENT_DIR / "posts.json").write_text(json.dumps(posts, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"posts": posts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
