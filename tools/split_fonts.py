"""把華康 woff2 依字碼切成多個小檔，搭配 @font-face 的 unicode-range 使用。

為什麼要切：一套華康約 3MB，顧問用手機 4G 開網頁要等好幾秒才看得到正確字型。
切成約 500 字一包之後，瀏覽器只會下載姓名實際用到的那幾包（通常 2～3 包、每包約 100KB）。

用法：python3 tools/split_fonts.py fonts/DFHeiMediumP.woff2 fonts/DFHeiMediumP
輸出：<輸出資料夾>/NN.woff2 與 manifest.json（[{file, range}]，range 是 CSS unicode-range 字串）
"""
import json
import os
import sys

from fontTools import subset
from fontTools.ttLib import TTFont

CHUNK = 500


def ranges_css(cps):
    """把排序過的字碼壓成 U+XXXX-YYYY 形式，unicode-range 越短，瀏覽器比對越快。"""
    out, start, prev = [], cps[0], cps[0]
    for c in cps[1:]:
        if c == prev + 1:
            prev = c
            continue
        out.append((start, prev))
        start = prev = c
    out.append((start, prev))
    return ", ".join(f"U+{a:X}" if a == b else f"U+{a:X}-{b:X}" for a, b in out)


def main(src, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    cps = sorted(c for c in TTFont(src).getBestCmap() if c >= 0x20)
    # 拉丁字母、數字、標點放第一包：幾乎每個名字都會用到空白和間隔號
    basic = [c for c in cps if c < 0x2E80]
    cjk = [c for c in cps if c >= 0x2E80]
    groups = [basic] + [cjk[i:i + CHUNK] for i in range(0, len(cjk), CHUNK)]

    manifest = []
    for i, group in enumerate(groups):
        name = f"{i:02d}.woff2"
        opts = subset.Options()
        opts.flavor = "woff2"
        opts.layout_features = ["*"]
        opts.notdef_outline = True
        font = TTFont(src)
        sub = subset.Subsetter(options=opts)
        sub.populate(unicodes=group)
        sub.subset(font)
        font.flavor = "woff2"
        font.save(os.path.join(out_dir, name))
        manifest.append({"file": name, "range": ranges_css(group)})
    with open(os.path.join(out_dir, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False)
    print(out_dir, len(groups), "chunks")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
