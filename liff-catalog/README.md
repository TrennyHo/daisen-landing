# 呆森 配件・濾芯 目錄（LIFF）

在 LINE 裡打開的商品目錄。客人選自己的 Dyson 機型，只看得到能用的品項，
點「詢問這項」回到聊天室、訊息已預填，按送出後由既有的 bot 接手。

**沒有購物車，也沒有動到 `bots/daisen/app.py`。** 成交流程完全走原本的對話。

## 網址

- 頁面：`https://trennyho.github.io/daisen-landing/liff-catalog/`
- 商品 API：`https://line-bot-admin-478147972022.asia-east1.run.app/api/daisen/public/products`

## 資料從哪來

商品**即時讀後台**（`line-bot-admin` 的公開唯讀端點 → GCS `daisen-products.json`）。
在後台「產品／服務項目」改價、加商品、停用，目錄頁下次載入就會反映，**不用改這裡的程式，也不用重新部署**。

那個端點只回傳啟用中商品的公開欄位（名稱、分類、價格、適用、說明），
不含 `id` / 時間戳，也不需要登入 —— 這些內容官網型錄本來就公開了。

## 機型篩選怎麼判斷

後台的「適用」欄位是自由文字，由 API 端的 `models_from_needs()` 解析：

| 適用欄位 | 解析成 |
|---|---|
| `V6 / V7 / V8` | V6, V7, V8 |
| `V12 Slim` | V12 |
| `V10 日版短款` | V10 |
| `V6-V15 全系列` | 全部機型 |

**V6 只有 2 項適用**（主機清潔保養 + 前置濾網），所有吸頭配件都是 V7 以後的快拆規格。
頁面遇到品項 ≤ 3 項時會先解釋原因再列，不會讓人以為壞掉。

## 圖片

`images.json` 是「商品名 → 縮圖」的靜態對照，縮圖在 `thumbs/`。
官網原圖平均 200KB，22 張就是 4.3MB；縮成 168px 後總共 165KB。

官網換圖或新增商品後重跑：

```bash
cd brands/03_呆森清潔/liff-catalog && python3 make_thumbs.py
```

腳本會比對後台 API 的商品名稱，對不上的會印出來。
目前 23 項裡 22 項有圖，只有「主機清潔保養」沒有（它是服務，卡片本來就是另一種樣式）。

## LIFF

`index.html` 裡的 `LIFF_ID` 目前是空的，填了才會啟用 LIFF SDK。

沒有 LIFF ID 也能正常瀏覽 —— 「詢問這項」會走 `line.me/R/oaMessage/@daisen?<預填訊息>`，
跟官網型錄的 `lineAsk()` 同一招。有 LIFF ID 時會優先用 `liff.sendMessages()` 直接送出，
少按一次。

**`liff.sendMessages()` 從圖文選單開啟時不能用**（LINE 的限制，只有從聊天室開才行），
所以預填訊息那條退路一定要留著，不能拿掉。

## 刻意沒做的事

- **不顯示運費。** 運費規則現在散在 `bots/daisen/app.py` 的 SYSTEM_PROMPT 和包裹卡片上，
  寫在這裡就是第八個會過期的地方。目錄只負責讓客人找到東西，運費讓 bot 在對話裡講。
  如果之後要顯示，記得一併加進 `bots/daisen/CLAUDE.md` 的價格連動清單。
- **不做購物車。** Ethan 明確不要。
