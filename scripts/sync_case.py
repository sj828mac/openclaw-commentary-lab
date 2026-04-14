#!/usr/bin/env python3
from __future__ import annotations

import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
SOURCE_ROOT = WORKSPACE / "openclaw-commentary-mvp" / "cases"
POSTS_DIR = ROOT / "posts"
CONTENT_DIR = ROOT / "content"
TOPICS_CONFIG = CONTENT_DIR / "topics.json"


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    parts: list[str] = []
    in_list = False
    for raw in lines:
        line = raw.rstrip()
        if not line:
            if in_list:
                parts.append("</ul>")
                in_list = False
            continue
        escaped = html.escape(line)
        if line.startswith("# "):
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("> "):
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif line.startswith("- "):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{html.escape(line[2:])}</li>")
        else:
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<p>{escaped}</p>")
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def wrap_page(title: str, style: str, description: str, content_html: str) -> str:
    template = (ROOT / "templates" / "post-template.html").read_text(encoding="utf-8")
    return (
        template.replace("{{TITLE}}", title)
        .replace("{{STYLE}}", style)
        .replace("{{DESCRIPTION}}", description)
        .replace("{{CONTENT}}", content_html)
    )


def build_post(topic: dict, variant: dict) -> dict:
    source_file = SOURCE_ROOT / topic["sourceDir"] / variant["source"]
    md = source_file.read_text(encoding="utf-8")
    out_name = f"{variant['slug']}.html"
    html_page = wrap_page(
        variant["title"],
        variant["style"],
        variant["description"],
        md_to_html(md),
    )
    (POSTS_DIR / out_name).write_text(html_page, encoding="utf-8")
    return {
        "slug": variant["slug"],
        "title": variant["title"],
        "style": variant["style"],
        "description": variant["description"],
        "topic": topic["topic"],
        "status": "published",
        "path": f"posts/{out_name}",
    }


def main() -> int:
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    topics = json.loads(TOPICS_CONFIG.read_text(encoding="utf-8"))
    posts: list[dict] = []
    for topic in topics:
        for variant in topic.get("variants", []):
            posts.append(build_post(topic, variant))
    (CONTENT_DIR / "posts.json").write_text(json.dumps(posts, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"topics": topics, "posts": posts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
