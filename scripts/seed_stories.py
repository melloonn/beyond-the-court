"""Initial editorial collection. Edit src/data/stories.json for future content."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-11-07'
STORIES = [
    ('lendeborg-home-for-mom', '5175737', '一個家的驚喜，獻給媽媽', '家庭', '當新秀的第一步，走回家人身邊。',
     ['ClutchPoints 在 2026 年 11 月 7 日報導，Yaxel Lendeborg 在 YouTube 影片中，送給媽媽一間新家。報導以家人聚在一起、迎接驚喜的片段，呈現他與母親的關係。',
      '這是他場外生活的一個公開切面，也讓球迷能在得分與籃板之外，看見家人的意義。關於「第一支影片」的說法，目前以媒體報導為限；本網站未獨立核對完整頻道上片歷史，因此不把它當成已確認的標題。'],
     'ClutchPoints', 'Watch Warriors rookie Yaxel Lendeborg surprise his mom with new house', 'https://clutchpoints.com/nba/golden-state-warriors/warriors-news-watch-yaxel-lendeborg-surprise-mom-house', '2026-11-07', None),
    ('curry-eat-learn-play', '3975', '把影響力留在 Oakland', '公益', '吃得好、讀得到、玩得開心：Curry 的另一張成績單。',
     ['Stephen 與 Ayesha Curry 的 Eat. Learn. Play. 基金會把工作重心放在 Oakland 孩子的營養、閱讀與運動機會。學校、社區與合作組織一起參與，是這項工作的核心。',
      '基金會的公開內容包含閱讀資源與校園遊戲空間。從球場回到社區，這些計畫提供了一個理解 Curry 影響力的角度；計畫細節與最新進度可由下方基金會原始資料繼續閱讀。'],
     'Eat. Learn. Play.', '基金會使命與工作', 'https://www.eatlearnplay.org/', None, None),
    ('curry-underrated-golf', '3975', '三分線之外，還有下一個發球台', '興趣', '從高爾夫熱情，延伸出給年輕球員的機會。',
     ['Curry 對高爾夫的投入，也延伸到 UNDERRATED Golf。計畫希望降低參與門檻，讓更多年輕選手能獲得比賽與發展機會。',
      '官方網站列有美國、歐洲巡迴賽及 Curry Cup 資訊。這裡把高爾夫作為他公開的場外投入來介紹；巡迴賽賽事與 NBA 比賽數據分開呈現。'],
     'UNDERRATED Golf / Eat. Learn. Play.', 'UNDERRATED Golf 官方網站', 'https://www.underrated.golf/', None, None),
    ('curry-li-ning-partnership', '3975', 'Curry Brand 的下一章', '品牌', '一份有日期可查的合作公告，連起籃球與高爾夫。',
     ['LI-NING 在 2026 年 6 月發布與 Stephen Curry、Curry Brand 的長期合作公告，涵蓋產品共同開發與運動文化計畫。公告提到的方向包含籃球、高爾夫與生活運動品類。',
      '本篇記錄這次已宣布的合作，不把過去的品牌關係自動視為仍在進行。合作內容可能調整，後續應依品牌與球員的新公告更新。'],
     'LI-NING / PR Newswire', 'LI-NING Announces Long-Term Partnership with Stephen Curry and Curry Brand', 'https://www.prnewswire.com/news-releases/li-ning-announces-long-term-partnership-with-stephen-curry-and-curry-brand-302787789.html', '2026-06-01', '2026-06-01'),
    ('butler-bigface', '6430', 'Jimmy 的另一個主場，聞起來像咖啡', '品牌', 'BIGFACE 讓球員的個性，走進咖啡與設計。',
     ['Jimmy Butler 的 BIGFACE 是他的場外事業。品牌官方網站持續公開產品、活動與合作資訊，呈現他在籃球之外投入咖啡的另一面。',
      '從球員頁走到品牌故事，可以看見不同於比賽訪問的生活興趣。這是人物介紹，商品價格、門市與合作消息請以品牌最新公告為準。'],
     'BIGFACE', 'BIGFACE 官方新聞與活動', 'https://www.bigfacebrand.com/pages/news-press', None, None),
    ('green-on-the-mic', '6589', '終場哨響之後，麥克風打開', '影音', '在 The Draymond Green Show，聽球員自己說。',
     ['Draymond Green 透過 The Draymond Green Show 分享比賽觀點、對話與場外故事。節目提供了一個由球員自己解釋場上經驗的入口。',
      '節目中的評價與預測屬於個人觀點，與官方比賽紀錄分開閱讀。網站保留節目的原始入口，讓讀者可以回到完整內容，理解發言的上下文。'],
     'The Draymond Green Show / Apple Podcasts', '節目官方介紹與集數', 'https://podcasts.apple.com/us/podcast/the-draymond-green-show/id1595716948', None, None),
    ('payton-learning-differently', '3134903', '學習的方式不同，夢想一樣大', '公益', 'Gary Payton II 把自己的經驗，化為對孩子的支持。',
     ['Gary Payton II Foundation 關注閱讀障礙的認識、早期篩檢與支持。他把成長中面對學習困難的經驗，帶進與孩子及家庭的交流。',
      '基金會公開的活動包含閱讀障礙宣導與社區服務。這些工作讓人看到他在防守與灌籃之外，如何運用自己的平台，幫助孩子理解自己、找到支持。'],
     'Gary Payton II Foundation', '基金會使命與社區活動', 'https://gpiifoundation.org/', None, None),
    ('moody-motivate-one', '4432171', '讓下一個孩子，看見更多可能', '公益', '從 Little Rock 出發的 Motivate One。',
     ['NBPA Foundation 的人物介紹記錄，Moses Moody 在 2022 年成立 Motivate One Foundation，關注青少年的領導力、生活能力與成長機會。',
      '其社區工作包含職涯工作坊、青年活動及開學資源支持。這些計畫把他與家鄉、灣區的連結，延伸到籃球以外的生活選擇。'],
     'NBPA Foundation', 'Moses Moody 董事介紹', 'https://www.nbpafoundation.com/board-modes-moody', None, None),
    ('podziemski-baseball-roots', '4709138', '曾經握球棒的那個男孩', '成長', 'Podziemski 的競爭心，有一部分來自棒球場。',
     ['San Francisco Chronicle 的專訪回顧，Brandin Podziemski 成長時曾同時參與棒球與籃球，之後才把重心轉向籃球。父親也在報導中分享了這段選擇。',
      '從不同運動走向職業籃球，是理解他成長背景的一條線索。這裡整理的是求學與家庭故事，不把其他運動經驗直接當作球場表現的因果解釋。'],
     'San Francisco Chronicle', 'Santa Clara’s star guard went from Illinois’ bench to one of WCC’s best in a year', 'https://www.sfchronicle.com/sports/college/article/Santa-Clara-s-star-guard-went-from-Illinois-17726185.php', None, None),
    ('melton-next-generation', '4066436', '把自己的經驗，傳給下一代', '公益', 'Something Light Assassins 的青少年籃球計畫。',
     ['Something Light Assassins 官方網站介紹，這項青少年籃球計畫由 De’Anthony Melton 在 2025 年創辦，重視基本功、團隊合作與品格發展。',
      '計畫把他在青少年籃球與職業賽場累積的經驗，帶進訓練與指導。這裡介紹其公開使命，並未假設每項活動都免費或屬於慈善捐贈。'],
     'Something Light Assassins', '計畫使命與成立背景', 'https://somethinglightassassinsbasketball.com/', None, None),
    ('richard-beyond-football', '4897262', '從美式足球家庭，走向自己的球場', '成長', 'Will Richard 的選擇，從另一項運動說起。',
     ['Florida Gators 的人物專題提到，Will Richard 的父親曾在 Clemson 打美式足球，他自己也曾參與這項運動，之後走向籃球。',
      '大學的專題讓人看見他的家庭背景與選擇。將這段成長史放在職業數據旁，可以認識球員走到 NBA 前的路，而不只記得選秀順位。'],
     'Florida Gators', 'The Skinny on Will Richard', 'https://floridagators.com/news/2024/3/8/mens-basketball-heres-the-skinny-on-will-richard-march-9-2024', '2024-03-08', None),
    ('santos-brasilia-roots', '4997536', '從 Brasília 出發，帶著家鄉上場', '成長', 'Gui Santos 與巴西的連結，留在生活與記憶裡。',
     ['巴西媒體 Globo Esporte 的專訪介紹 Gui Santos 與出生城市 Brasília 的關係，包括他對當地地標、生活與家人的記憶。',
      '跟隨父親的職業籃球生涯移動、再走向自己的旅程，是這段背景的一部分。比賽表格記錄每次出賽，家鄉故事則補上他從哪裡來。'],
     'Globo Esporte', 'A relação de Gui Santos com Brasília', 'https://ge.globo.com/df/noticia/2024/07/16/tatuagens-da-ponte-jk-da-catedral-e-mergulho-no-lago-paranoa-a-relacao-de-gui-santos-com-brasilia.ghtml', '2024-07-16', None),
    ('horford-give-back-home', '3213', '把籃球機會，帶回多明尼加', '公益', 'Al Horford 與家鄉年輕球員的連結。',
     ['NBA 的官方公告記錄，Al Horford 參與在多明尼加推動 Jr. NBA 訓練營。計畫除了基本技術，也重視團隊合作、尊重與社區價值。',
      '這是一項有歷史公告可查的社區投入。本篇記錄已發生的工作，不把舊訓練營公告當作目前仍開放報名的活動。'],
     'NBA Communications', 'Al Horford 與多明尼加首屆 Jr. NBA 訓練營', 'https://pr.nba.com/al-horford-jr-nba-dominican-republic/', None, None),
    ('niang-charity-golf', '2990969', '用一場高爾夫，延續 Iowa 的連結', '公益', 'Georges Niang 的場外投入，也走上果嶺。',
     ['Friendship Ark 的活動頁保留了 2021 年 Georges Niang Charity Golf Outing 的資訊，呈現他透過高爾夫活動支持社區組織的一面。',
      '本篇是歷史活動介紹，並非當年度活動預告。與 Curry 不同的高爾夫故事，也提醒我們：球員的社區連結往往延續自求學或成長的地方。'],
     'Friendship Ark', '2021 Georges Niang Charity Golf Outing', 'https://www.friendshipark.org/niang_golf_outing', None, None),
    ('porzingis-court-at-home', '3102531', '送給家鄉，一座可以一起打球的球場', '公益', 'Porzingis 與 Liepāja 的籃球連結。',
     ['Liepāja Olympic Centre 的公開資料記錄，Kristaps Porzingis 在 2016 年 6 月 15 日向家鄉捐建戶外籃球場。場地讓在地居民有更多參與籃球的空間。',
      '這項歷史紀錄呈現他的家鄉投入。它與目前的身體狀態、出賽或球隊安排無關；這些不同類型的資訊，在網站中各自保留來源與時間。'],
     'Liepāja Olympic Centre', 'KP6 Basketball Court', 'https://loc.lv/en/stadiums/kp6-basketball-court/', None, '2016-06-15'),
    ('bassey-lagos-journey', '4397886', '從 Lagos 的街頭，到職業球場', '成長', '在成為籃球員之前，Bassey 的日常還有足球。',
     ['Charles Bassey 的成長專訪回顧，他在奈及利亞曾幫家人賣炸雞，也喜歡踢足球；後來被教練注意到，開始接觸籃球。',
      '這段跨越國家的成長經歷，補上 NBA 數據之前的背景。原始專訪有更多他離家、適應生活與學習籃球的細節，可以從下方連結繼續閱讀。'],
     'CloseUp360', 'Charles Bassey: From Soccer Player and Food Vendor in Nigeria to Premiere NBA Draft Prospect', 'https://closeup360.com/features/charles-bassey-from-soccer-player-food-vendor-in-nigeria-to-premiere-nba-draft-prospect/', '2021-07-14', None),
    ('williams-next-step', '4397040', '繞過傷停，繼續尋找下一個機會', '成長', 'Brandon Williams 在 Arizona 之後的選擇。',
     ['Arizona 在 2020 年的官方公告記錄，Brandon Williams 決定探索職業機會，離開大學球隊。公告也回顧了他因膝蓋手術而經歷的休養。',
      '這是他的生涯背景，不代表目前有相同傷勢。從大學到職業的路並非每個人都一樣，讀這段故事時，也能回到生涯表格看看他後來的出賽足跡。'],
     'University of Arizona Athletics', 'Brandon Williams To Pursue Professional Opportunities', 'https://arizonawildcats.com/news/2020/9/4/mens-basketball-brandon-williams-to-pursue-professional-opportunities', '2020-09-04', '2020-09-04'),
    ('cryer-close-to-home', '4433149', '離家更近，向目標再走一步', '成長', 'LJ Cryer 在 Houston 的學習與選擇。',
     ['University of Houston 的專題回顧 LJ Cryer 從 Baylor 轉往 Houston 的經歷。他希望持續進步，也在新的環境接受防守與團隊要求的挑戰。',
      'Houston 與他成長的 Katy 距離不遠，讓這段求學旅程也帶著家鄉色彩。文章記錄的是大學時期的背景，不把大學成績混入 NBA 生涯統計。'],
     'University of Houston', 'UH Basketball: It’s All About The Little Things', 'https://stories.uh.edu/magazine/magazine/online-stories/basketball-march-madness-2024/index.html', None, None),
    ('leons-far-from-home', '4897449', '離家四千英里，重新找到自己的團隊', '成長', '從荷蘭到美國，Malevy Leons 的求學旅程。',
     ['Mineral Area College 的校友專訪回顧，Malevy Leons 在 2019 年離開荷蘭家鄉，到美國追求大學籃球目標。他需要適應不同的生活，也想念家人。',
      '隊友、同學與社區成為他新的支持網絡。這段旅程呈現跨國球員在籃球之外的適應與關係，也讓讀者認識職業球場前的他。'],
     'Mineral Area College', 'Malevy Leons - Centennial Alumni Spotlight', 'https://mineralarea.edu/news/malevy-leons-centennial-alumni-spotlight/', '2022-12-13', None),
    ('ike-family-name', '4703396', '一個名字，一段與祖父的連結', '家庭', 'Graham Ike 把家人的影響帶在身上。',
     ['The Spokesman-Review 在 2025 年的專訪，介紹 Graham Ike 名字與祖父 Tom Graham 的關係，也回顧祖父在家庭與待人處事上對他的影響。',
      '專題以他在 Gonzaga 更換球衣號碼的背景切入，讓人認識一位年輕球員如何記住家人。本篇記錄當時的故事，現役背號則以球員頁的名單快照為準。'],
     'The Spokesman-Review', 'Graham Ike’s switch to No. 15 at Gonzaga and a tribute to a man who beat the odds', 'https://www.spokesman.com/stories/2025/oct/23/graham-ikes-switch-to-no-15-at-gonzaga-and-a-tribu/', '2025-10-23', None),
]

stories = []
for sid, pid, title, category, summary, paragraphs, publisher, source_title, url, published, event_date in STORIES:
    sources = [{'publisher': publisher, 'title': source_title, 'url': url, 'publishedAt': published}]
    if sid == 'curry-underrated-golf':
        sources.append({'publisher': 'Eat. Learn. Play.', 'title': 'Curry 家庭公益與高爾夫專訪', 'url': 'https://www.eatlearnplay.org/news/inside-philanthropy-feb-14-2024', 'publishedAt': '2024-02-14'})
    stories.append({'id': sid, 'playerIds': [pid], 'title': title, 'category': category, 'summary': summary,
                    'paragraphs': paragraphs, 'eventDate': event_date, 'publishedAt': DATE,
                    'verifiedAt': DATE, 'sources': sources})
path = ROOT / 'src/data/stories.json'
path.parent.mkdir(parents=True, exist_ok=True)
if path.exists():
    raise SystemExit('Content exists; edit stories.json directly. Seed does not overwrite edits.')
path.write_text(json.dumps(stories, ensure_ascii=False, indent=2) + '\n')
print('Created', len(stories), 'original editorial summaries')
