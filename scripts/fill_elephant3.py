# -*- coding: utf-8 -*-
"""
填充续篇2：电弱区内部结构 / Σ分裂 / 核整数关系 / μ因子家族检查
追加到 大象脊线填充报告.md
"""
import math, os

PHI = (1 + math.sqrt(5)) / 2
ETA = (1 + math.sqrt(3)) / 2
ME = 0.51099895
MU = 105.6583755
BASE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(BASE, "大象脊线填充报告.md")

EW = {"W": 80369.2, "Z": 91187.6, "H": 125250, "t": 172760}
EWI = {"W": 157279, "Z": 178450, "H": 245108, "t": 338083}
HEAVY = [
    ("D0", 1864.84), ("Ds", 1968.35), ("Lambda_c", 2286.46), ("Xi_c", 2467.9),
    ("eta_c", 2983.9), ("J/psi", 3096.9), ("chi_c0", 3414.75), ("psi(2S)", 3686.10),
    ("B0", 5279.66), ("B+", 5279.34), ("Bs", 5366.88), ("Lambda_b", 5619.60),
    ("Bc", 6274.9), ("Y(1S)", 9460.30), ("Y(2S)", 10023.26), ("Y(3S)", 10355.2),
    ("W", 80369.2), ("Z", 91187.6), ("H", 125250), ("t", 172760),
]
SIGMA = {"Sigma+": 1189.37, "Sigma0": 1192.642, "Sigma-": 1197.449}
NUCLEI_INT = {"p": 1836, "n": 1839, "d": 3670, "t": 5497, "He3": 5496, "alpha": 7294}

L = []
L.append("")
L.append("---")
L.append("")
L.append("## 十一、电弱区内部结构（续填 · 自主运行）")
L.append("")
# H ≈ sqrt(Z*t)
hz = math.sqrt(EW["Z"] * EW["t"])
L.append(f"### H ≈ √(Z·t)")
L.append(f"√(m_Z·m_t) = √({EW['Z']}×{EW['t']}) = {hz:.0f} MeV；m_H = {EW['H']} MeV；偏差 {(hz/EW['H']-1)*100:.3f}%")
L.append(f"整数版：√(n_Z·n_t) = √({EWI['Z']}×{EWI['t']}) = {math.sqrt(EWI['Z']*EWI['t']):.0f}；n_H = {EWI['H']}；偏差 {(math.sqrt(EWI['Z']*EWI['t'])/EWI['H']-1)*100:.3f}%")
L.append("")
# H/(W+Z) ≈ sqrt3 - 1
r1 = (EW["W"] + EW["Z"]) * (math.sqrt(3) - 1)
L.append(f"### H/(W+Z) ≈ √3−1")
L.append(f"(m_W+m_Z)(√3−1) = ({EW['W']}+{EW['Z']})×0.732051 = {r1:.0f} MeV；m_H = {EW['H']}；偏差 {(r1/EW['H']-1)*100:.3f}%")
L.append("")
# EW ratio scan
L.append("### 电弱整数比 vs 体系常数")
L.append("")
pairs = [("Z/W", EWI["Z"]/EWI["W"]), ("H/Z", EWI["H"]/EWI["Z"]), ("t/H", EWI["t"]/EWI["H"]),
         ("t/Z", EWI["t"]/EWI["Z"]), ("H/W", EWI["H"]/EWI["W"]), ("t/W", EWI["t"]/EWI["W"])]
consts = {"phi": PHI, "eta": ETA, "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3),
          "sqrt3-1": math.sqrt(3)-1, "phi/sqrt3": PHI/math.sqrt(3), "eta^2": ETA**2,
          "phi^2": PHI**2, "14/9": 14/9, "1.9": 1.9, "phi^4/8": PHI**4/8}
for name, val in pairs:
    best = min(consts.items(), key=lambda kv: abs(kv[1]-val)/val)
    L.append(f"{name} = {val:.5f} → 最近常数 {best[0]} = {best[1]:.5f}（偏差 {abs(best[1]-val)/val*100:.3f}%）")
L.append("")
L.append("## 十二、Σ 分裂在整数格上")
L.append("")
si = [round(m/ME) for m in SIGMA.values()]
L.append(f"Σ+ = {si[0]}，Σ0 = {si[1]}，Σ− = {si[2]}；分裂 {si[1]-si[0]}、{si[2]-si[1]}（m_e 单位）")
L.append(f"实测：Σ0−Σ+ = {SIGMA['Sigma0']-SIGMA['Sigma+']:.3f} MeV = {(SIGMA['Sigma0']-SIGMA['Sigma+'])/ME:.2f}·m_e；"
         f"Σ−−Σ0 = {SIGMA['Sigma-']-SIGMA['Sigma0']:.3f} MeV = {(SIGMA['Sigma-']-SIGMA['Sigma0'])/ME:.2f}·m_e")
L.append("")
L.append("## 十三、核整数关系")
L.append("")
L.append(f"p = {NUCLEI_INT['p']}，n = {NUCLEI_INT['n']}，d = {NUCLEI_INT['d']}")
L.append(f"d = p + n − 5：{NUCLEI_INT['p']}+{NUCLEI_INT['n']}−5 = {NUCLEI_INT['p']+NUCLEI_INT['n']-5} ✓（5 = 2D 投影计数）")
L.append(f"α = 2p + 2n − 56：2×{NUCLEI_INT['p']}+2×{NUCLEI_INT['n']}−56 = {2*NUCLEI_INT['p']+2*NUCLEI_INT['n']-56} ✓（56 = 2³×7；α 结合能 55.4·m_e，差 1.1%）")
L.append("")
L.append("## 十四、重粒子 μ 因子家族检查")
L.append("")
L.append("| 粒子 | m/m_μ | 最近整数 | 偏差 | 备注 |")
L.append("|---|---|---|---|---|")
for name, m in HEAVY:
    r = m / MU
    ni = round(r)
    dev = abs(r - ni) / r * 100
    note = ""
    if dev < 2:
        note = f"≈ {ni}·m_μ（{dev:.2f}%）"
    L.append(f"| {name} | {r:.3f} | {ni} | {dev:.2f}% | {note} |")
L.append("")
L.append("结论：B0 ≈ 50·m_μ（0.06%）、Y(1S) ≈ 89.5·m_μ（0.04%）是孤点，未成家族；重粒子主格是整数格。")
L.append("")

text = "\n".join(L)
with open(REPORT, "a", encoding="utf-8") as f:
    f.write(text)
print(text)
