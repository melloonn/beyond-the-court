# Beyond the Court｜勇士場上場下

每個數字背後，都有一個人。這個繁體中文籃球專題從金州勇士出發，把全隊球員的場上數據、生涯與場外故事放在同一個網站。

## 第一版內容

- 18 位名單球員，每人有獨立網址與個人頁。
- 本季平均、近期出賽、全部有紀錄賽季的 NBA 例行賽／季後賽逐季平均及總計、來源 Career 列。
- 本季 9 場已完賽紀錄、完整雙方 box score、逐節得分及球隊比較。
- 20 篇原創人物摘要：家庭、公益、興趣、品牌、影音與成長；每位球員至少一篇。
- 搜尋中英文名與背號、位置／本季出賽篩選、得分／時間／背號排序、生涯切換與 CSV 匯出。
- 52 個靜態 HTML 頁面，響應式排版，無第三方程式套件、無資料庫、無 API key。

資料為 2026-11-07 取得的 2026–27 例行賽快照；最近比賽為美東 11/5、台北 11/6 的 MIA–GSW。不是即時比分。當前名單與涵蓋範圍以 `src/data/teams/golden-state-warriors.json` 為準。

## 本機執行

需要 Python 3.9+；Node.js 僅用於 JavaScript 語法檢查，不需 npm install。

```sh
python3 scripts/validate.py --data-only
python3 scripts/build.py
python3 scripts/validate.py
python3 -m http.server 8765 --directory dist --bind 127.0.0.1
```

開啟 <http://127.0.0.1:8765>。不需連上統計服務即可從現有資料建置。

## 更新資料

```sh
python3 scripts/refresh_data.py
python3 scripts/validate.py --data-only
python3 scripts/build.py
python3 scripts/validate.py
node --check src/assets/main.js
node --test tests/interaction.test.cjs
```

匯入器使用 Python 標準函式庫讀取 ESPN 公開資料，來源可能限制存取，無法保證一直可用。只在整批候選資料通過檢查且圖片取得成功後替換網站資料。原始回應的網址、UTC 時間與 SHA-256 保存在 `data/raw/manifest.json`。不在前端放置憑證，不在瀏覽時依賴即時統計 API。

`scripts/seed_stories.py` 僅用於初次產生編輯內容，不會覆蓋已存在的故事檔。後續請直接編輯 `src/data/stories.json`。

## 專案規則與擴充

先閱讀 [AGENTS.md](AGENTS.md)。它定義專案目的、頁面格式、設計、命名、資料查核、擴充流程、測試與發布要求。

- 新增故事：在 `src/data/stories.json` 加入完整紀錄，以 `playerIds` 連接人物。重新建置後，自動出現於故事列表與球員頁。
- 新增球員：匯入名單、基本資料、逐季統計與近期紀錄，補上有來源的人物故事。共用模板會產生個人頁與球隊卡片。
- 新增球隊：建立球隊資料與來源對應，再將入口與模板中的球隊設定抽出；不可複製勇士數字。本版完整實作勇士，其他球隊尚未建立。

擴充範例見 [docs/extension-guide.md](docs/extension-guide.md)，資料定義與更正政策見 [docs/data-policy.md](docs/data-policy.md)，查核紀錄見 [docs/data-audit.md](docs/data-audit.md)。

## 驗證範圍

`scripts/validate.py` 驗證名單、ID、欄位寬度、逐季範圍、命中數、百分比範圍、出賽紀錄、勝負、得分公式、雙方球員得分合計、故事引用、原始快照雜湊，以及全站內部頁面、錨點與本機資產。數學一致不代表所有歷史資料都經獨立逐列查核；抽查範圍與限制在查核紀錄中說明。

## 圖片與權利

球員肖像來源與使用限制見 [docs/assets.md](docs/assets.md)。網站非 NBA／球隊官方網站。球員照片、姓名與品牌屬各權利人，本專案不提供第三方素材的再授權。故事為自行整理的摘要並附原始出處。

## 作業繳交

繳交用文字及新增內容說明見 [docs/submission.md](docs/submission.md)。GitHub Repository 與公開網址將於實際發布成功後填入。

## GitHub Pages 發布

經確認後，使用 `python3 scripts/build.py --pages` 將輸出同步至 `docs/`，保留既有說明文件。GitHub Pages 來源設定為 `main` 分支的 `/docs`，不需 GitHub Actions、npm 或伺服器。變更資料後，重新建置並提交新的 `docs/` 才會更新公開網站。`dist/` 是本機建置輸出，列入 gitignore；`docs/` 是公開發布輸出，需提交。
