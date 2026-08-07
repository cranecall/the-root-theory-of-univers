# -*- coding: utf-8 -*-
"""
框架"回归不分裂"纹理：有向循环(A→B→C→A) + 闭合耦合 d((3,1)非零)
M = [[0, a, d], [a, m2, c], [d, c, m3]]
a = √(m1m2), c = √(m2m3)（循环边 = 几何平均，η原则）
d = 闭合耦合（"我们"极闭合环 —— 框架的自由度）
扫描 d，看 V_cb 能否达到实测 0.0412
"""
import numpy as np

m_u, m_c, m_t = 2.16, 1263, 173950
m_d, m_s, m_b = 4.45, 95.9, 4271

def matrix_cycle(m1, m2, m3, d_frac):
    a = np.sqrt(m1 * m2)
    c = np.sqrt(m2 * m3)
    d = d_frac * np.sqrt(m1 * m3)   # d 以全几何平均为刻度
    M = np.array([[0.0, a, d], [a, m2, c], [d, c, m3]])
    return M

def ckm(mat_u, mat_d):
    wu, Uu = np.linalg.eigh(mat_u)
    wd, Ud = np.linalg.eigh(mat_d)
    return np.abs(Uu.T @ Ud), wu, wd

measured = {"Vus": 0.2253, "Vcb": 0.0412, "Vub": 0.0038, "Vtd": 0.0089}

print("扫描闭合耦合 d（d = d_frac × √(m1m3)）：\n")
print(f"{'d_frac':>7} | {'V_us':>7} {'V_cb':>7} {'V_ub':>7} {'V_td':>7} | {'Vcb偏':>7} {'Vus偏':>7}")
best = None
for frac in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
    Mu = matrix_cycle(m_u, m_c, m_t, frac)
    Md = matrix_cycle(m_d, m_s, m_b, frac)
    C, wu, wd = ckm(Mu, Md)
    # 质量检查（中间代不能为0）
    if abs(wu[1]) < 10 or abs(wd[1]) < 1:
        print(f"{frac:7.1f} | 中间代质量为0，纹理奇异")
        continue
    vus, vcb, vub, vtd = C[0, 1], C[1, 2], C[0, 2], C[2, 0]
    cb_dev = (vcb - measured["Vcb"]) / measured["Vcb"] * 100
    us_dev = (vus - measured["Vus"]) / measured["Vus"] * 100
    print(f"{frac:7.1f} | {vus:7.4f} {vcb:7.4f} {vub:7.4f} {vtd:7.4f} | {cb_dev:7.1f}% {us_dev:7.1f}%")
    if best is None or abs(cb_dev) + abs(us_dev) < best[0]:
        best = (abs(cb_dev) + abs(us_dev), frac, vus, vcb, vub, vtd)

print()
if best:
    print(f"最佳: d_frac={best[1]} → V_us={best[2]:.4f} V_cb={best[3]:.4f} V_ub={best[4]:.4f} V_td={best[5]:.4f}")
    print(f"实测:        V_us=0.2253  V_cb=0.0412  V_ub=0.0038  V_td=0.0089")
