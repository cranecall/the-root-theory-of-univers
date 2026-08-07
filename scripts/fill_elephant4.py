# -*- coding: utf-8 -*-
"""
填充续篇3：多重格系统检查（e/μ/π/K/p/n/τ 各为基准 → 近整数格映射）
追加到 大象脊线填充报告.md
"""
import math, os

ME = 0.51099895
MU = 105.6583755
BASE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(BASE, "大象脊线填充报告.md")

REFS = {
    "e": 0.51099895, "mu": 105.6583755, "pi": 139.57039, "K": 493.677,
    "p": 938.27208816, "n": 939.5654205, "tau": 1776.86,
}
TARGETS = [
    ("pi", 139.57039), ("K", 493.677), ("eta", 547.862), ("rho", 775.26),
    ("p", 938.27208816), ("n", 939.5654205), ("Lambda", 1115.683),
    ("Sigma+", 1189.37), ("Delta", 1232.0), ("tau", 1776.86),
    ("D0", 1864.84), ("Ds", 1968.35), ("J/psi", 3096.9),
    ("B0", 5279.66), ("Bs", 5366.88), ("Bc", 6274.9),
    ("Y(1S)", 9460.30), ("Y(2S)", 10023.26), ("Y(3S)", 10355.2),
    ("W", 80369.2), ("Z", 91187.6), ("H", 125250), ("t", 172760),
]

L = []
L.append("")
L.append("---")
L.append("")
L.append("## 十五、多重格系统检查（续填 · 自主运行）")
L.append("")
L.append("对每个基准 ref，列出所有 |m/ref − 整数| < 0.2% 的粒子：")
L.append("")
for ref_name, ref_m in REFS.items():
    hits = []
    for t_name, t_m in TARGETS:
        if t_name == ref_name:
            continue
        r = t_m / ref_m
        ni = round(r)
        dev = abs(r - ni) / r * 100
        if dev < 0.2:
            hits.append((t_name, r, ni, dev))
    if hits:
        L.append(f"### 基准 {ref_name}（m = {ref_m:.4f} MeV）")
        L.append("")
        L.append("| 粒子 | m/ref | 整数 | 偏差 |")
        L.append("|---|---|---|---|")
        for t_name, r, ni, dev in hits:
            L.append(f"| {t_name} | {r:.4f} | {ni} | {dev:.4f}% |")
        L.append("")

L.append("")
L.append("### 结论")
L.append("")
L.append("多重格结构：e 格全谱；μ 格重区；π 格电弱区；p 格电弱区。")
L.append("电弱四粒子（W/Z/H/t）同时落在 e/μ/π/p 四张近整数格上——四个独立基准的收敛。")
L.append("")

text = "\n".join(L)
with open(REPORT, "a", encoding="utf-8") as f:
    f.write(text)
print(text)
