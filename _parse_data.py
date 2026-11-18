# -*- coding: utf-8 -*-
"""解析新榜单数据，输出统计信息 + 导出 JSON。"""
import openpyxl, json, statistics, datetime

SRC = r"C:/Users/siliconli/Desktop/新榜单数据.xlsx"
OUT_JSON = r"c:/Users/siliconli/CodeBuddy/20260920195118/rank_data.json"

wb = openpyxl.load_workbook(SRC, read_only=True, data_only=True)
ws = wb["Sheet1"]
rows = list(ws.iter_rows(values_only=True))
data = rows[1:]

# 字段: 0日期 1modid 2玩法名 3首次上架 4days 5new 6week 7ret 8rev 9cum 10add 11fd 12fc 13score 14rank
recs = []
for x in data:
    recs.append({
        "date": str(x[0])[:10],
        "modid": str(x[1]),
        "name": str(x[2]),
        "first_date": str(x[3])[:10],
        "days": int(x[4]),
        "new": int(x[5]),
        "week": int(x[6]),
        "ret": int(x[7]),
        "rev": int(x[8]),
        "cum": int(x[9]),
        "add": round(float(x[10]), 6),
        "fd": round(float(x[11]), 6),
        "fc": round(float(x[12]), 6),
        "score": round(float(x[13]), 6),
        "rank": int(x[14]),
    })

print("总数:", len(recs), "日期:", sorted(set(r["date"] for r in recs)))
print("rank范围:", min(r["rank"] for r in recs), "-", max(r["rank"] for r in recs))

days = [r["days"] for r in recs]
cum = [r["cum"] for r in recs]
new = [r["new"] for r in recs]
rev = [r["rev"] for r in recs]
add = [r["add"] for r in recs]
fd = [r["fd"] for r in recs]
fc = [r["fc"] for r in recs]

print("days: min=%d med=%.0f max=%d  >180=%d" % (min(days), statistics.median(days), max(days), sum(1 for d in days if d > 180)))
print("cum:  min=%d med=%.0f max=%d  >1500万=%d" % (min(cum), statistics.median(cum), max(cum), sum(1 for c in cum if c > 15000000)))
print("new:  min=%d med=%.0f max=%d" % (min(new), statistics.median(new), max(new)))
print("rev:  min=%d med=%.0f max=%d" % (min(rev), statistics.median(rev), max(rev)))
print("add:  min=%.3f med=%.3f max=%.3f" % (min(add), statistics.median(add), max(add)))
print("fd:   min=%.3f med=%.3f max=%.3f" % (min(fd), statistics.median(fd), max(fd)))
print("fc:   min=%.3f med=%.3f max=%.3f" % (min(fc), statistics.median(fc), max(fc)))

print("\n前15名:")
for r in recs[:15]:
    print("%3d %-12s days=%-4d new=%8d rev=%9d cum=%9d add=%.3f fd=%.3f fc=%.3f score=%.4f"
          % (r["rank"], r["name"], r["days"], r["new"], r["rev"], r["cum"], r["add"], r["fd"], r["fc"], r["score"]))

# 典型样本：加分项高但排名靠后的（被衰减压制）
print("\n加分项最高的10个玩法（观察衰减影响）:")
top_add = sorted(recs, key=lambda r: -r["add"])[:10]
for r in top_add:
    print("%3d %-12s days=%-4d cum=%9d add=%.3f fd=%.3f fc=%.3f score=%.4f"
          % (r["rank"], r["name"], r["days"], r["cum"], r["add"], r["fd"], r["fc"], r["score"]))

# 保存 JSON
with open(OUT_JSON, "w", encoding="utf-8") as f:
    json.dump(recs, f, ensure_ascii=False)
print("\n已导出:", OUT_JSON, "共", len(recs), "条")
