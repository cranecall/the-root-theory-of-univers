# -*- coding: utf-8 -*-
"""
填充续篇4：投影层全谱普查（剩余粒子/原子核/夸克质量 → 整数格）
例外 = 不在格上的粒子。追加到 大象脊线填充报告.md
"""
import math, os

ME = 0.51099895
MU = 105.6583755
BASE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(BASE, "大象脊线填充报告.md")

# (name, mass MeV)
EXTRA = [
    # 介子剩余
    ("K*+", 891.67), ("K*0", 895.55), ("h1(1170)", 1170.0), ("b1(1235)", 1229.5),
    ("a1(1260)", 1230.0), ("f1(1285)", 1281.9), ("f2(1270)", 1275.4),
    ("eta_c(2S)", 3637.5), ("chi_c1", 3510.67), ("chi_c2", 3556.17),
    ("hc(1P)", 3525.38), ("psi(3770)", 3773.13), ("D*", 2010.26), ("Ds*", 2112.2),
    ("B*", 5324.7), ("Bs*", 5415.4), ("eta_b", 9399.0),
    ("Upsilon(4S)", 10579.4), ("chi_b0", 9859.44), ("chi_b1", 9892.78), ("chi_b2", 9912.21),
    # 重子剩余
    ("Sigma_c", 2453.5), ("Omega_c", 2695.2), ("Xi_b", 5794.5), ("Omega_b", 6045.4),
    # 原子核
    ("d", 1875.613), ("t", 2808.921), ("He3", 2808.391), ("alpha", 3727.379),
    ("Li7", 6534.7), ("Be9", 8392.8), ("B11", 10252.7), ("C12", 11174.9),
    ("O16", 14895.1), ("Fe56", 52103.5),
    # 夸克（MS-bar）
    ("u(MSbar)", 2.16), ("d(MSbar)", 4.67), ("s(MSbar)", 93.4),
    ("c(MSbar)", 1270), ("b(MSbar)", 4180),
]

L = []
L.append("")
L.append("---")
L.append("")
L.append("## 十六、投影层全谱普查（续填 · 自主运行）")
L.append("")
L.append("### 在格上的（|m/m_e − 整数| < 0.5%）")
L.append("")
L.append("| 粒子 | 质量 MeV | n = m/m_e | 整数 | 偏差 |")
L.append("|---|---|---|---|---|")
on = []
off = []
for name, m in EXTRA:
    n = m / ME
    ni = round(n)
    dev = abs(n - ni) / n * 100
    if dev < 0.5:
        on.append((name, m, n, ni, dev))
    else:
        off.append((name, m, n, ni, dev))
for name, m, n, ni, dev in on:
    L.append(f"| {name} | {m:.4f} | {n:.2f} | {ni} | {dev:.4f}% |")
L.append("")
L.append(f"在格上：{len(on)}/{len(EXTRA)}")
L.append("")
L.append("### 例外（不在格上，偏差 ≥ 0.5%）")
L.append("")
L.append("| 粒子 | 质量 MeV | n = m/m_e | 最近整数 | 偏差 |")
L.append("|---|---|---|---|---|")
for name, m, n, ni, dev in off:
    L.append(f"| {name} | {m:.4f} | {n:.2f} | {ni} | {dev:.2f}% |")
L.append("")
L.append("### μ 格（重粒子，m > 1.8 GeV）")
L.append("")
L.append("| 粒子 | m/m_μ | 整数 | 偏差 |")
L.append("|---|---|---|---|")
for name, m, n, ni, dev in on:
    if m > 1800:
        r = m / MU
        ri = round(r)
        rdev = abs(r - ri) / r * 100
        L.append(f"| {name} | {r:.3f} | {ri} | {rdev:.3f}% |")
L.append("")

text = "\n".join(L)
with open(REPORT, "a", encoding="utf-8") as f:
    f.write(text)
print(text)
