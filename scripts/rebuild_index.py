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
      <div class="badge">OpenClaw Commentary Lab</div>
      <h1>OpenClaw 技術追蹤評論</h1>
      <p>聚焦 agent platform、記憶系統、repo understanding 與工作流工具的追蹤型評論。這裡不是單純列新聞，而是整理哪些專案真的值得長期觀察，哪些問題正在暴露平台的真實難點。</p>
      <div class="meta">
        <span>GitHub Repo 追蹤</span>
        <span>Agent Platform 分析</span>
        <span>GitHub Pages</span>
      </div>
    </section>

    <section class="quick-nav">
      <a href="posts/index.html">
        <div class="quick-nav-card">
          <div class="kicker">快速入口</div>
          <h3>進入文章索引</h3>
          <p>查看所有長文、短版快評與渠道變體文章。</p>
        </div>
      </a>
      <a href="topics/index.html">
        <div class="quick-nav-card">
          <div class="kicker">快速入口</div>
          <h3>進入主題索引</h3>
          <p>查看所有主題頁與追蹤主題入口。</p>
        </div>
      </a>
    </section>

    <h2>精選文章</h2>
    <section class="grid">
      <article class="card">
        <div class="kicker">編輯推薦</div>
        <h3><a href="posts/recent-github-repos-editorial.html">最近在追的 3 個 GitHub repo</a></h3>
        <p>從 Onyx、Harness 到 Humanizer-zh-TW，對照 AI 平台、工程治理與文字修整三種不同節奏。</p>
        <div class="meta"><span>適合第一次進站先讀</span><span>站內總覽入口</span></div>
      </article>
      <article class="card">
        <div class="kicker">編輯推薦</div>
        <h3><a href="posts/hermes-agent-editorial.html">Hermes Agent 值得追，不只是因為它大</a></h3>
        <p>它真正值得看的，不只是功能面，而是平台摩擦如何開始浮出來。</p>
        <div class="meta"><span>平台案例</span><span>追蹤重點明確</span></div>
      </article>
      <article class="card">
        <div class="kicker">編輯推薦</div>
        <h3><a href="posts/hermes-vs-openclaw-editorial.html">Hermes Agent vs OpenClaw</a></h3>
        <p>一個像大平台，一個像高可塑 runtime。這篇看的是兩種不同的 agent 平台哲學。</p>
        <div class="meta"><span>對比閱讀</span><span>適合建立全局觀</span></div>
      </article>
      <article class="card">
        <div class="kicker">編輯推薦</div>
        <h3><a href="posts/agent-platform-tracking-method-editorial.html">我怎麼追 Agent Platform 類 GitHub Repo</a></h3>
        <p>不是只看 stars、commit 與 release，而是看 gateway、sub-agent 與 provider abstraction。</p>
        <div class="meta"><span>方法論</span><span>適合延伸追站內其他文章</span></div>
      </article>
    </section>

    <h2>最新追蹤</h2>
    <section class="grid">
      <article class="card">
        <div class="kicker">Latest Tracking</div>
        <h3><a href="posts/evolver-editorial.html">EvoMap Evolver</a></h3>
        <p>一個試圖把 agent 自我演化、錯誤修補與 Hub / Worker / Proxy 鏈路推進到工程現場的高概念平台樣本。</p>
        <div class="meta"><span>高概念平台案例</span><span>最新加入</span></div>
      </article>
      <article class="card">
        <div class="kicker">Latest Tracking</div>
        <h3><a href="posts/graphify-editorial.html">Graphify</a></h3>
        <p>跨 AI coding assistant 的知識圖譜層，值得觀察 query、MCP 與性能邊界。</p>
        <div class="meta"><span>結構化上下文</span><span>持續追蹤</span></div>
      </article>
      <article class="card">
        <div class="kicker">Latest Tracking</div>
        <h3><a href="posts/mempalace-editorial.html">MemPalace</a></h3>
        <p>AI 記憶系統如何從 benchmark 敘事走向可信的工程現場。</p>
        <div class="meta"><span>記憶系統</span><span>持續追蹤</span></div>
      </article>
    </section>

    <h2>主題入口</h2>
    <section class="grid">
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/hermes-agent.html">Hermes Agent</a></h3>
        <p>從大型 agent 工具轉向通用 agent platform 的平台化樣本。</p>
      </article>
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/hermes-vs-openclaw.html">Hermes Agent vs OpenClaw</a></h3>
        <p>兩種不同的 agent 平台哲學：大平台整合與高可塑 runtime。</p>
      </article>
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/recent-github-repos.html">最近在追的 3 個 GitHub repo</a></h3>
        <p>Onyx、Harness、Humanizer-zh-TW 的對照觀察。</p>
      </article>
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/graphify.html">Graphify</a></h3>
        <p>跨 AI coding assistant 的 knowledge graph / repo understanding 候選基礎層。</p>
      </article>
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/mempalace.html">MemPalace</a></h3>
        <p>AI 記憶系統如何從 benchmark 敘事走向可信的工程現場。</p>
      </article>
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/ai-hedge-fund.html">AI Hedge Fund</a></h3>
        <p>多 agent 金融研究 workflow 從 viral demo 走向工程現實的樣板。</p>
      </article>
      <article class="card">
        <div class="kicker">Topic</div>
        <h3><a href="topics/evolver.html">EvoMap Evolver</a></h3>
        <p>自我演化敘事如何進入 Hub / Worker / Proxy 與 session scope 的工程現場。</p>
      </article>
      <article class="card">
        <div class="kicker">Method</div>
        <h3><a href="topics/agent-platform-tracking-method.html">追蹤方法論</a></h3>
        <p>我怎麼判斷一個 repo 是在長功能，還是在長平台。</p>
      </article>
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
