#!/usr/bin/env python3
"""從官網型錄 products.html 抽出「商品名 → 圖片」，產生縮圖與 images.json。

官網原圖平均 200KB，這頁只用 56px 縮圖，直接掛原圖等於讓手機下載 4.3MB。
產成 168px（3 倍圖）後總共約 165KB。

官網新增商品、換圖之後重跑：
    cd brands/03_呆森清潔/liff-catalog && python3 make_thumbs.py

注意名稱對照的坑（bots/daisen/CLAUDE.md 也有記）：
官網濾芯卡是 card-name「後置濾網」+ card-models「V7 / V8」分兩段，
後台名稱是合併的「後置濾網 V7／V8」而且用全形斜線；
吸頭配件的後台名稱則不含機型。所以兩種組合都要試、斜線要正規化。
"""
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent                      # repo 根目錄，官網原圖在這層
THUMB_PX = 168                          # 版面顯示 56px，取 3 倍圖
JPEG_QUALITY = "72"

CARD_RE = re.compile(
    r'<img class="card-img" src="([^"]+)"[^>]*>.*?'
    r'<div class="card-name">([^<]+)</div>\s*'
    r'(?:<div class="card-models">([^<]*)</div>)?',
    re.S,
)


def norm(s: str) -> str:
    return re.sub(r"\s+", "", s).replace("/", "／")


def main() -> int:
    html = (ROOT / "products.html").read_text(encoding="utf-8")

    resp = subprocess.run(
        ["curl", "-sf",
         "https://line-bot-admin-478147972022.asia-east1.run.app/api/daisen/public/products"],
        capture_output=True, text=True,
    )
    if resp.returncode != 0:
        print("讀不到後台商品 API，無法比對名稱。", file=sys.stderr)
        return 1
    products = json.loads(resp.stdout)
    by_norm = {norm(p["name"]): p["name"] for p in products}

    thumbs = HERE / "thumbs"
    thumbs.mkdir(exist_ok=True)

    mapping, unmatched = {}, []
    for src, name, models in CARD_RE.findall(html):
        name, models = name.strip(), (models or "").strip()
        # 吸頭配件後台名稱不含機型，濾芯含 → 兩種都試
        matched = next((by_norm[c] for c in (norm(name), norm(name + models)) if c in by_norm), None)
        if not matched:
            unmatched.append(f"{name} {models}".strip())
            continue
        dst = thumbs / (pathlib.Path(src).stem + ".jpg")
        subprocess.run(
            ["sips", "-Z", str(THUMB_PX), "-s", "format", "jpeg",
             "-s", "formatOptions", JPEG_QUALITY, str(ROOT / src), "--out", str(dst)],
            capture_output=True, check=True,
        )
        mapping[matched] = "thumbs/" + dst.name

    (HERE / "images.json").write_text(
        json.dumps(mapping, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    total = sum((HERE / v).stat().st_size for v in mapping.values())
    print(f"{len(mapping)} 張縮圖，共 {total // 1024} KB")
    if unmatched:
        print("官網有卡片但後台對不到名稱：", unmatched, file=sys.stderr)
    no_image = sorted({p["name"] for p in products} - set(mapping))
    if no_image:
        print("後台有商品但官網沒圖（會顯示純文字卡片）：", no_image)
    return 0


if __name__ == "__main__":
    sys.exit(main())
