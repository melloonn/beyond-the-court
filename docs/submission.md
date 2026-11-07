# 作業繳交資料

標題：`學校 學號 系級 姓名 Beyond the Court｜勇士場上場下`

請在繳交前補上自己的學校、學號、系級與姓名。

## 1. 專案簡介
我製作了一個結合場上數據與場外故事的籃球網站「Beyond the Court｜勇士場上場下」。第一版以金州勇士為主，涵蓋 18 位球員的個人頁、本季與 NBA 生涯數據、近期比賽，以及家庭、公益、興趣、品牌與成長故事。每份資料都保留來源，並標示快照時間。

## 2. GitHub Repository
[melloonn/beyond-the-court](https://github.com/melloonn/beyond-the-court)

## 3. 網頁連結
[Beyond the Court｜勇士場上場下](https://melloonn.github.io/beyond-the-court/)

## 4. AGENTS.md
Repository 根目錄的 `AGENTS.md` 定義專案目的、頁面結構、設計風格、檔案格式、資料正確性、AI 修改規則、擴充流程與測試。公開網站頁尾也提供文件入口。

[直接閱讀 AGENTS.md](https://github.com/melloonn/beyond-the-court/blob/main/AGENTS.md)

## 5. 規則如何幫助 AI 繼續完成？
球員、比賽與故事分開以結構化資料管理，共用同一套頁面模板。新增故事時，AI 依照 AGENTS.md 查核來源、填寫固定欄位並連接球員 ID，重新建置後就會自動產生新頁，並更新故事列表與球員頁。新增球員沿用相同統計欄位與模板，不必重新設計版面。

第一版已使用同一格式建立 Curry 的公益、高爾夫與品牌合作三篇文章，並為全隊 18 人產生個人頁，展示規則可重複使用。資料驗證工具會檢查 ID、引用、比分、統計格式與連結，降低日後擴充時出錯的機會。
