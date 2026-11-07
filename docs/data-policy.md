# 資料政策

## 統計範圍與來源
本版以 ESPN 的同次公開資料匯入為準，名單含全部 18 位球員，包含雙向合約與尚無本季出賽紀錄的人。NBA 官方名單與 Basketball Reference 用於交叉抽查。主要來源：

- 名單：`https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/gs/roster`
- 賽程：`https://site.api.espn.com/apis/site/v2/sports/basketball/nba/teams/gs/schedule?season=2027&seasontype=2`
- 球員：`https://site.web.api.espn.com/apis/common/v3/sports/basketball/nba/athletes/{id}/stats?seasontype={2|3}`
- 近期紀錄：同上 `/gamelog?season=2027`
- 比賽：`https://site.api.espn.com/apis/site/v2/sports/basketball/nba/summary?event={id}`

公開端點不是供應商對本專案的穩定 API 保證。不得繞過驗證、付費牆或存取限制；不可在瀏覽器公開任何憑證。快照網站可在來源中斷時繼續閱讀。

## 欄位契約
球員：`id, slug, name, number, position, height, birthDate, college, headshot, regular, playoffs, recent, retrievedAt, sources`。`regular/playoffs` 的各 category 包含 `name, labels, names, rows, career`；每列有 `season, year, team, teamId, values`，欄位寬度必須一致。保留供應商顯示精度與合計。

球隊：`id, slug, name, nameZh, season, seasonYear, seasonType, wins, losses, playerIds, gameIds, latestGameAt, retrievedAt, sources`。

比賽：`id, date, season, seasonType, status, venue, teams, boxscore, teamStats, source, retrievedAt`。

故事：`id, playerIds, title, category, summary, paragraphs, eventDate, publishedAt, verifiedAt, sources`。分類限 `公益/家庭/興趣/品牌/影音/成長`。故事來源有 `title, url, publisher, publishedAt`，日期不明可為 null。本站發布日、來源發布日與事件日不同。

## 計算與空值
- 球隊場均由所有已完賽比賽的總量除以場數。籃板／助攻使用全隊統計，不假設球員籃板相加等於球隊籃板。
- 球員平均與生涯 Career 列沿用供應商。總計與平均不可相加；轉隊全季合計列與單隊列不可再相加。
- 零出手命中率顯示「—」；無出賽顯示「本季尚無出賽紀錄」。
- ESPN 在新秀無季後賽時可能默默回傳例行賽資料。必須檢查 `seasontype` 的值與可選項，確認沒有季後賽選項才輸出無紀錄狀態。
- 近期列表可能略去上場時間四捨五入為 0 的實際出賽；以 box score 的 `didNotPlay=false` 補齊，記錄 `reconciledFromBoxscore=true` 及來源。補充命中率以該場總命中／出手計算；零出手仍顯示「—」。
- 附加賽、熱身賽、G League、大學與國家隊資料不得混入。

## 新聞與更正
原創摘要，保留來源與查核日。優先本人、品牌、基金會、學校與聯盟公告；媒體報導標示其名稱。不複製報導全文，不把傳聞、歷史合作或來源未確認的描述當作現況。未獨立核對 Lendeborg 頻道歷史前，不宣稱該影片為其第一支影片。

發現衝突先查截止時間、賽季、統計口徑與官方更正；無法解決的資訊暫不當作確定事實。變更需記錄來源與原因，重新驗證、建置與發布。

## 公開介面與查核紀錄
依專案介面需求，公開 HTML 不展示資料取得、統計截止、編輯或查核日期；仍顯示賽季、實際比賽日期、事件日期、來源連結與非即時性質。JSON、data/raw/manifest.json 及 Repository 查核文件完整保留原始時間，隱藏介面日期不代表數據即時更新。
