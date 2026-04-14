#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "posts.json"


def render_cards(posts: list[dict]) -> str:
    parts: list[str] = []
    for post in posts:
        parts.append(
            f'''      <article class="card">\n        <div class="kicker">{post["style"]}</div>\n        <h3><a href="{post["path"]}">{post["title"]}</a></h3>\n        <p>{post["description"]}</p>\n        <div class="meta"><span>Topic: {post["topic"]}</span><span>Status: {post["status"]}</span></div>\n      </article>'''
        )
    return "\n".join(parts)


def main() -> int:
    posts = json.loads(CONTENT.read_text(encoding="utf-8"))
    cards = render_cards(posts)
    index = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OpenClaw Commentary Lab</title>
  <link rel="stylesheet" href="styles.css" />
</head>
<body>
  <div class="container">
    <section class="hero">
      <div class="badge">OpenClaw Commentary Lab · Internal Testing</div>
      <h1>OpenClaw 技術追蹤評論 Blog</h1>
      <p>用來測試追蹤型評論的 GitHub Pages Blog。把同一主題發佈成不同風格頁面，方便比較語氣、結構與可讀性。</p>
      <div class="meta">
        <span>Repo-based publishing</span>
        <span>GitHub Pages</span>
        <span>Internal validation first</span>
      </div>
    </section>

    <section class="grid">
{cards}
    </section>
  </div>

  <footer>
    <div class="container">OpenClaw Commentary Lab · <a href="posts/index.html">Posts Index</a></div>
  </footer>
</body>
</html>
'''
    (ROOT / "index.html").write_text(index, encoding="utf-8")
    posts_index = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Posts · OpenClaw Commentary Lab</title>
  <link rel="stylesheet" href="../styles.css" />
</head>
<body>
  <div class="container article">
    <section class="hero" style="padding-top:48px;">
      <div class="badge">Posts Index</div>
      <h1>評論文章索引</h1>
      <p>所有已發布測試文章都會收錄於此。</p>
    </section>
    <section class="grid">
{cards.replace('href="posts/','href="')}
    </section>
    <p><a href="../index.html">← 回首頁</a></p>
  </div>
</body>
</html>
'''
    (ROOT / "posts" / "index.html").write_text(posts_index, encoding="utf-8")
    print(f"rebuilt index for {len(posts)} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
