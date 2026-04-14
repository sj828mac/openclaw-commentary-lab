#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
POSTS_JSON = CONTENT / "posts.json"
TOPICS_JSON = CONTENT / "topics.json"
TOPICS_DIR = ROOT / "topics"


def render_post_cards(posts: list[dict], relative: bool = False) -> str:
    parts: list[str] = []
    for post in posts:
        href = post["path"]
        if relative and href.startswith("posts/"):
            href = href[len("posts/"):]
        parts.append(
            f'''      <article class="card">\n        <div class="kicker">{post["style"]}</div>\n        <h3><a href="{href}">{post["title"]}</a></h3>\n        <p>{post["description"]}</p>\n        <div class="meta"><span>Topic: {post["topic"]}</span><span>Status: {post["status"]}</span></div>\n      </article>'''
        )
    return "\n".join(parts)


def render_topic_cards(topics: list[dict], relative: bool = False) -> str:
    parts: list[str] = []
    for topic in topics:
        href = f"topics/{topic['topic']}.html"
        if relative:
            href = f"{topic['topic']}.html"
        parts.append(
            f'''      <article class="card">\n        <div class="kicker">Topic</div>\n        <h3><a href="{href}">{topic["title"]}</a></h3>\n        <p>{topic["description"]}</p>\n      </article>'''
        )
    return "\n".join(parts)


def write_topic_pages(topics: list[dict], posts: list[dict]) -> None:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for post in posts:
        grouped[post["topic"]].append(post)
    TOPICS_DIR.mkdir(parents=True, exist_ok=True)
    for topic in topics:
        cards = []
        for post in grouped.get(topic["topic"], []):
            cards.append(
                f'''      <article class="card">\n        <div class="kicker">{post["style"]}</div>\n        <h3><a href="../{post["path"]}">{post["title"]}</a></h3>\n        <p>{post["description"]}</p>\n      </article>'''
            )
        page = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Topic · {topic["title"]}</title>
  <link rel="stylesheet" href="../styles.css" />
</head>
<body>
  <div class="container article">
    <section class="hero" style="padding-top:48px;">
      <div class="badge">Topic Page</div>
      <h1>{topic["title"]}</h1>
      <p>{topic["description"]}</p>
    </section>
    <div class="grid">
{"\n".join(cards)}
    </div>
    <p><a href="index.html">← 回主題索引</a></p>
  </div>
</body>
</html>
'''
        (TOPICS_DIR / f"{topic['topic']}.html").write_text(page, encoding="utf-8")


def main() -> int:
    posts = json.loads(POSTS_JSON.read_text(encoding="utf-8"))
    topics = json.loads(TOPICS_JSON.read_text(encoding="utf-8"))
    post_cards = render_post_cards(posts)
    topic_cards = render_topic_cards(topics)

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
      <p>用來測試追蹤型評論的 GitHub Pages Blog。現已支援多主題、多風格頁面與主題索引。</p>
      <div class="meta">
        <span>Repo-based publishing</span>
        <span>GitHub Pages</span>
        <span>Multi-topic ready</span>
      </div>
    </section>

    <h2>主題</h2>
    <section class="grid">
{topic_cards}
    </section>

    <h2>最新文章</h2>
    <section class="grid">
{post_cards}
    </section>
  </div>

  <footer>
    <div class="container">OpenClaw Commentary Lab · <a href="posts/index.html">Posts Index</a> · <a href="topics/index.html">Topics Index</a></div>
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
{render_post_cards(posts, relative=True)}
    </section>
    <p><a href="../index.html">← 回首頁</a></p>
  </div>
</body>
</html>
'''
    (ROOT / "posts" / "index.html").write_text(posts_index, encoding="utf-8")

    topics_index = f'''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Topics · OpenClaw Commentary Lab</title>
  <link rel="stylesheet" href="../styles.css" />
</head>
<body>
  <div class="container article">
    <section class="hero" style="padding-top:48px;">
      <div class="badge">Topics Index</div>
      <h1>主題索引</h1>
      <p>所有可追蹤與可發佈的評論主題。</p>
    </section>
    <section class="grid">
{render_topic_cards(topics, relative=True)}
    </section>
    <p><a href="../index.html">← 回首頁</a></p>
  </div>
</body>
</html>
'''
    (TOPICS_DIR / "index.html").write_text(topics_index, encoding="utf-8")

    write_topic_pages(topics, posts)
    print(f"rebuilt site for {len(topics)} topics and {len(posts)} posts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
