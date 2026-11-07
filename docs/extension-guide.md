# 讓 AI 繼續擴充的方式

先給 AI 這個指令：

> 閱讀 AGENTS.md 與 docs/data-policy.md，依現有格式新增指定內容。先確認來源及日期，沿用共用模板，完成後執行資料驗證、建置與全站連結檢查。

## 示例：替 Curry 新增一篇活動故事

1. 閱讀本人或活動方公告，確認活動日期、角色與報導日期。
2. 在 `src/data/stories.json` 追加以下格式，使用原創摘要：

```json
{
  "id": "curry-new-community-event",
  "playerIds": ["3975"],
  "title": "依照已查證活動填寫標題",
  "category": "公益",
  "summary": "有來源的活動摘要",
  "paragraphs": ["自行整理的背景與事件。", "有出處的活動細節。"],
  "eventDate": null,
  "publishedAt": "填入本站編輯日期",
  "verifiedAt": "填入實際查核日期",
  "sources": [
    {"publisher": "原始發布者", "title": "原始標題", "url": "填入已查證的 HTTPS 網址", "publishedAt": null}
  ]
}
```

這是格式示意，不能直接把占位文字發布成文章。`eventDate` 只能在知道實際日期時填值。

3. 執行 `python3 scripts/validate.py --data-only`、`python3 scripts/build.py`、`python3 scripts/validate.py`。
4. 新故事自動生成 `stories/<id>.html`，並出現在故事列表與 Curry 頁。無須到各 HTML 手動貼卡片。
5. 檢查類別篩選、球員連結、來源與手機版後，才更新公開站點。

## 實際的重複使用證據
本版 Curry 的公益、高爾夫與 LI-NING 合作三篇內容，共用相同資料格式與模板；另外 17 位球員使用同一個個人頁模板。從球員連到故事，從故事回到生涯資料，都由穩定 ID 自動建立。

## 新增球隊的下一步
本版專注勇士。新增球隊時，先建立正確的 team ID 與來源對應，將 `scripts/build.py` 的球隊入口、hero 焦點人物與文案抽為球隊設定，再沿用現有卡片、表格及故事模板；資料驗證也要改為按該球隊 ID 執行。不要僅複製勇士檔案、改標題後保留原數字。
