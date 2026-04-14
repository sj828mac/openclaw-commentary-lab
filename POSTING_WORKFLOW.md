# Posting Workflow

## 目標
讓 commentary-mvp 的案例內容，可以快速同步到 GitHub Pages Blog。

## 現在的做法

### 來源
案例內容放在：
- `../openclaw-commentary-mvp/cases/<topic>/`

目前已對接：
- `ai-hedge-fund`

### Blog 輸出
執行：
```bash
cd /home/sj/.openclaw/workspace/projects/openclaw-commentary-lab
./publish.sh
```

它會做三件事：
1. 從 `openclaw-commentary-mvp/cases/ai-hedge-fund/` 同步內容
2. 重建首頁與 posts 索引
3. commit + push 到 GitHub

## 新增新主題時
1. 先在 commentary-mvp 裡完成 case 資料夾
2. 調整 `scripts/sync_case.py` 讓它知道新的來源檔案
3. 執行 `./publish.sh`

## 三種頁面風格
- Editorial：長文評論版
- Quick Take：短版快評版
- Channel Variants：渠道變體版

## 後續可擴充
- 支援多 topic 自動掃描
- 支援日期、tag、系列頁
- 支援從 markdown frontmatter 自動建頁
- 支援 cron 自動同步
