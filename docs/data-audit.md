# 第一版查核紀錄

查核日：2026-11-07。資料時間與原始 SHA-256 以 `data/raw/manifest.json` 為準。

## 已驗證
- ESPN 名單共 18 人，與當日 NBA 官方名單交叉核對；沒有將「本季未出賽」排除在名單外。
- 全體球員分別取得 NBA 逐季例行賽與季後賽平均、總計及來源提供的生涯 Career 列。
- Curry 2009–10：80 場、17.5 分、4.5 籃板、5.9 助攻；2015–16：79 場、30.1 分、5.4 籃板、6.7 助攻。與 Basketball Reference 抽查一致。
- Curry 2026–27：7 場、29.9 分、3.7 籃板、4.4 助攻；與當日 NBA 球員頁的場均摘要交叉核對一致。
- 勇士 9 場完賽、6 勝 3 敗；逐場的球員得分合計等於球隊比分，得分公式 `2×FGM + 3PM + FTM` 一致。
- 同季轉隊球員保留來源的單隊與合計列，不進行額外加總。
- 無季後賽選項時，不使用 ESPN 回退的例行賽資料冒充季後賽紀錄。
- Leons 有一場實際出賽的時間被四捨五入為 0，球員 gamelog 未列出；已從同場 box score 補入並保留來源旗標，與 DNP 區分。
- 20 篇人物故事附來源，每位球員至少一篇；歷史活動與本站編輯日期分開記錄。

## 查核來源
- [NBA 勇士名單](https://www.nba.com/team/1610612744/warriors/roster)
- [NBA Curry 個人頁](https://www.nba.com/player/201939/stephen-curry)
- [Basketball Reference Curry](https://www.basketball-reference.com/players/c/curryst01.html)
- 所有匯入的 ESPN 回應與網址見 `data/raw/manifest.json`。

## 限制
所有歷史列已做結構與數學合理性檢查，並非每一個歷史數值都逐一與第二家供應商人工核對。近期資料依公開來源與 box score，可能受來源更正影響。未完整核對 Lendeborg 的 YouTube 上片歷史，不把「第一支影片」作為已確認結論。公開網站與 GitHub Pages 部署已確認成功；瀏覽器畫面驗證受電腦控制權限限制，不將語法與 HTTP 檢查當作已完成視覺測試。
