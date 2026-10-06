"""修復華康 TTC 的 cmap：原始 format 4 子表最後一段的 glyphIdArray 偏移超界，
瀏覽器的字型安全檢查 (OTS) 會整個拒收。這裡手動寬鬆解析，丟掉超界的對應，
重建乾淨的 cmap，順便轉成 woff2 讓檔案小一點。"""
import struct, sys
from fontTools.ttLib import TTCollection, newTable
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4

def parse_fmt4(raw, off):
    seg2 = struct.unpack('>H', raw[off+6:off+8])[0]; seg = seg2 // 2
    length = struct.unpack('>H', raw[off+2:off+4])[0]
    p = off + 14
    ends = struct.unpack(f'>{seg}H', raw[p:p+seg2]); p += seg2 + 2
    starts = struct.unpack(f'>{seg}H', raw[p:p+seg2]); p += seg2
    deltas = struct.unpack(f'>{seg}h', raw[p:p+seg2]); p += seg2
    ro_base = p; ros = struct.unpack(f'>{seg}H', raw[p:p+seg2])
    end = off + length
    m, dropped = {}, 0
    for i in range(seg):
        for c in range(starts[i], ends[i] + 1):
            if c == 0xFFFF: continue
            if ros[i] == 0: g = (c + deltas[i]) & 0xFFFF
            else:
                a = ro_base + 2*i + ros[i] + 2*(c - starts[i])
                if a + 2 > end: dropped += 1; continue
                g = struct.unpack('>H', raw[a:a+2])[0]
                if g: g = (g + deltas[i]) & 0xFFFF
            if g: m[c] = g
    return m, dropped

src, idx, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
t = TTCollection(src, lazy=True).fonts[idx]
raw = t.reader['cmap']
n = struct.unpack('>H', raw[2:4])[0]
for k in range(n):
    pid, eid, o = struct.unpack('>HHI', raw[4+8*k:12+8*k])
    if (pid, eid) == (3, 1): break
mapping, dropped = parse_fmt4(raw, o)
# 原 cmap 壞了，fontTools 無法從它推出字形名稱，直接依數量編號
n = t['maxp'].numGlyphs
glyphs = ['.notdef'] + [f'g{i}' for i in range(1, n)]
t.setGlyphOrder(glyphs)
t['post'].formatType = 3.0
cmap = {c: glyphs[g] for c, g in mapping.items() if g < len(glyphs)}
sub = cmap_format_4(4); sub.platformID, sub.platEncID, sub.language, sub.cmap = 3, 1, 0, cmap
tbl = newTable('cmap'); tbl.tableVersion = 0; tbl.tables = [sub]
t['cmap'] = tbl
t.flavor = 'woff2'
t.save(out)
print(out, 'chars', len(cmap), 'dropped', dropped, '陳' in map(chr, cmap), '璿' in map(chr, cmap))
