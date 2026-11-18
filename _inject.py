# -*- coding: utf-8 -*-
import json
TMP = r"c:/Users/siliconli/CodeBuddy/20260920195118/_report_template.html"
SRC = r"c:/Users/siliconli/CodeBuddy/20260920195118/rank_data.json"
OUT = r"c:/Users/siliconli/CodeBuddy/20260920195118/玩法榜单排名汇报.html"

recs = json.load(open(SRC, encoding="utf-8"))
compact = [{k: r[k] for k in ("name","days","new","week","ret","rev","cum","add","fd","fc","score","rank")} for r in recs]

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
