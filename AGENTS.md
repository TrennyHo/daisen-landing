# 呆森 DaiSen 官網 — 給接手的人與 AI 工具

正式網址：https://trennyho.github.io/daisen-landing/
負責人：praperpro（GitHub `praperpro-nonbiri`），上線由 Ethan 決定。

**這是正在營業的店，不是 demo。** 真客人每天從包裹卡片、LINE 選單、bot 連進來。

## 先讀這份

完整的品牌定位、退換規則、品牌故事、價格規則、Dyson 機型對照，都在私有 repo
`sen-huo/senhuo-line` 的：

- `bots/daisen/CLAUDE.md`：**先讀「官網任務」那節**——定位句、目的、目標、可用的證據都在那裡
- `bots/daisen/dyson-機型對照.md`

這個 repo 是公開的，所以那些內容不放這裡。動手前先讀完那兩份。

**定位句：接近 Dyson 原廠的品質，不到一半的價格。** 官網開場第一眼就要看到。
現在的客人是在蝦皮買過呆森的人，多半從 LINE 打開型錄頁（手機），定位句之後接著講在 LINE 買的好處。
主要下單方式是 LINE OA，官網的按鈕都通到 LINE。

## 怎麼交

1. Fork 這個 repo 到自己帳號 → 開分支 → 改
2. 本機預覽：在資料夾裡跑 `python3 -m http.server 8000`，打開 http://localhost:8000
3. 手機寬度也要看（多數客人用手機）
4. 開 Pull Request 到 `TrennyHo/daisen-landing` 的 `main`，說明改了什麼、附截圖
5. Ethan 合併後**立刻上線**（GitHub Pages 自動部署），不用另外部署

## 四條紅線

1. **網址不能變**。`index.html`、`products.html` 不改檔名、不搬 repo——印好的卡片、LINE 選單、bot 都指著它們。
2. **這個 repo 是公開的**。`.gitignore` 是白名單：預設全擋，只放行網站用到的檔案。
   新增圖片要在 `.gitignore` 補一行 `!` 放行，否則 git 看不到。
   財務、印刷檔、品牌定位、客戶資料**絕對不能加進來**。
3. **價格不要寫死**。`products.html` 尾端的 `syncPrices()` 開頁時從後台讀價格，HTML 裡的數字只是備援。
   改價不在接手範圍內，由 Ethan 在後台改。後台新增的商品不會自動長出卡片，要手動加 HTML。
4. **呆森只賣副廠配件與濾芯**。清潔、保養、到府收件、超音波清洗都已永久停止，
   這些字眼與舊價格不能出現在網站上。文案也不要用「保證」「保障」。
