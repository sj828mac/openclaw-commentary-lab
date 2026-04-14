# Posting Workflow

## 目標
讓 commentary-mvp 的多個案例內容，可以快速同步到 GitHub Pages Blog。

## 現在的做法

### 來源
案例內容放在：
- `../openclaw-commentary-mvp/cases/<topic>/`

### Topic Registry
Blog 以 `content/topics.json` 作為來源設定。
每個 topic 定義：
- `topic`
- `title`
- `description`
- `sourceDir`
- `variants`

### Blog 輸出
執行：
```bash
cd /home/sj/.openclaw/workspace/projects/openclaw-commentary-lab
./publish.sh
```

它會做四件事：
1. 從 `openclaw-commentary-mvp/cases/` 同步所有已註冊 topic 內容
2. 重建首頁、posts 索引、topics 索引與每個 topic 頁
3. commit + push 到 GitHub
4. 發佈到 GitHub Pages

## 新增新主題時
1. 先在 commentary-mvp 裡完成 case 資料夾，例如：
   - `cases/<topic>/publish-ready-v1.md`
   - `cases/<topic>/short-post-v1.md`
   - `cases/<topic>/channel-variants.md`
2. 在 `content/topics.json` 加入新 topic 與 variants
3. 執行 `./publish.sh`

## 三種頁面風格
- Editorial：長文評論版
- Quick Take：短版快評版
- Channel Variants：渠道變體版

## 現在支援的索引頁
- `/` 首頁
- `/posts/index.html` 文章索引
- `/topics/index.html` 主題索引
- `/topics/<topic>.html` 單一主題頁

## 後續可擴充
- markdown frontmatter
- 自動讀取 cases 目錄
- 日期 / tags / 系列頁
- cron 自動同步
