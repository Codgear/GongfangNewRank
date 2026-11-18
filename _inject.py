# -*- coding: utf-8 -*-
import json, math
TMP = r"c:/Users/siliconli/CodeBuddy/20260920195118/_report_template.html"
SRC = r"c:/Users/siliconli/CodeBuddy/20260920195118/rank_data.json"
OUT = r"c:/Users/siliconli/CodeBuddy/20260920195118/玩法榜单排名汇报.html"

recs = json.load(open(SRC, encoding="utf-8"))

def _mms(vals):
    lo, hi = min(vals), max(vals)
    return [(v - lo) / (hi - lo) if hi > lo else 0 for v in vals]

_ln_new = [math.log(1 + r["new"]) for r in recs]
_ln_ret = [math.log(1 + r["ret"]) for r in recs]
_ln_rev = [math.log(1 + r["rev"]) for r in recs]
_nn = _mms(_ln_new); _nr = _mms(_ln_ret); _nv = _mms(_ln_rev)

compact = []
for _i, _r in enumerate(recs):
    _item = {k: _r[k] for k in ("name","days","new","week","ret","rev","cum","add","fd","fc","score","rank")}
    _item["an"] = round(0.35 * _nn[_i], 6)
    _item["ar"] = round(0.25 * _nr[_i], 6)
    _item["av"] = round(0.40 * _nv[_i], 6)
    compact.append(_item)

n = len(recs)
med_days = sorted(r["days"] for r in recs)[n//2]
med_fd = round(sorted(r["fd"] for r in recs)[n//2], 3)
over180 = sum(1 for r in recs if r["days"] > 180)
overcum = sum(1 for r in recs if r["cum"] > 15000000)
pct180 = round(over180/n*100)
pctfc = round((n-overcum)/n*100)

html = open(TMP, encoding="utf-8").read()
html = (html.replace("__DATA__", json.dumps(compact, ensure_ascii=False, separators=(",",":")))
            .replace("__N__", str(n))
            .replace("__MEDDAYS__", str(med_days))
            .replace("__MEDFD__", str(med_fd))
            .replace("__OVER180__", str(over180))
            .replace("__OVERCUM__", str(overcum))
            .replace("__PCT180__", str(pct180))
            .replace("__PCTFC__", str(pctfc)))
open(OUT, "w", encoding="utf-8").write(html)
print("已生成:", OUT, "| 玩法数:", n)
