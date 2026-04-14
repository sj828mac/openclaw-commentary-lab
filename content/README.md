# Content Registry

## `topics.json`
Blog 的主資料來源，定義：
- topic 名稱
- topic 描述
- sourceDir（對應 commentary-mvp/cases/<topic>/）
- variants（每個主題要產出的頁面）

## 擴充新主題
1. 在 `openclaw-commentary-mvp/cases/<topic>/` 建立內容檔案
2. 在 `content/topics.json` 加入新 topic 與 variants
3. 執行 `./publish.sh`

系統會自動：
- 同步所有主題
- 重建首頁
- 重建 posts 索引
- 重建 topics 索引
- push 到 GitHub Pages
