# -*- coding: utf-8 -*-
"""
框架纹理 + 相位：有向循环携带 CP 相位（非厄米/带相纹理）
M = [[0, a e^{iα}, d e^{iγ}], [a e^{-iα}, m2, c e^{iβ}], [d e^{-iγ}, c e^{-iβ}, m3]]
a=√(m1m2), c=√(m2m3)（循环边=几何平均）
d=闭合耦合（"我们"极），γ=闭合相位
先验证 Fritzsch（d=0, 带相）复现文献，再扫 (d, 相位差) 看 V_cb
"""
import numpy as np

m_u, m_c, m_t = 2.16, 1263, 173950
m_d, m_s, m_b = 4.45, 95.9, 4271

def tex(m1, m2, m3, alpha, beta, d_frac, gamma=0.0):
    a = np.sqrt(m1 * m2)
    c = np.sqrt(m2 * m3)
    d = d_frac * np.sqrt(m1 * m3)
    M = np.array([
        [0.0,           a*np.exp(1j*alpha), d*np.exp(1j*gamma)],
        [a*np.exp(-1j*alpha), m2,           c*np.exp(1j*beta)],
        [d*np.exp(-1j*gamma), c*np.exp(-1j*beta), m3],
    ])
    return M

def ckm_mag(Mu, Md):
    wu, Uu = np.linalg.eigh(Mu)
    wd, Ud = np.linalg.eigh(Md)
    return np.abs(Uu.conj().T @ Ud)

meas = {"Vus": 0.2253, "Vcb": 0.0412, "Vub": 0.0038, "Vtd": 0.0089}

print("=== 1. Fritzsch（d=0）带相位：验证文献 ===")
best_f = None
for phi in np.linspace(0, np.pi, 61):
    # 上扇相位 0，下扇相位 phi（相对相位差）
    Mu = tex(m_u, m_c, m_t, 0, 0, 0.0)
    Md = tex(m_d, m_s, m_b, phi/2, phi/2, 0.0)
    C = ckm_mag(Mu, Md)
    vus, vcb = C[0,1], C[1,2]
    err = abs(vus-meas["Vus"])/meas["Vus"] + abs(vcb-meas["Vcb"])/meas["Vcb"]
    if best_f is None or err < best_f[0]:
        best_f = (err, phi, vus, vcb, C[0,2], C[2,0])
print(f"最佳相位差 φ={best_f[1]:.2f}: V_us={best_f[2]:.4f} V_cb={best_f[3]:.4f} "
      f"V_ub={best_f[4]:.4f} V_td={best_f[5]:.4f}")
print(f"文献: V_us≈0.2144, V_cb 被强制 ≥0.064（若 V_us 对准 0.2253）\n")

print("=== 2. 框架变体：闭合耦合 d + 相位差 ===")
print(f"{'d':>6} {'φ':>6} | {'V_us':>7} {'V_cb':>7} {'V_ub':>7} {'V_td':>7} | 总偏差")
best = None
for d in [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    for phi in np.linspace(0, np.pi, 25):
        Mu = tex(m_u, m_c, m_t, 0, 0, d)
        Md = tex(m_d, m_s, m_b, phi/2, phi/2, d)
        C = ckm_mag(Mu, Md)
        vus, vcb, vub, vtd = C[0,1], C[1,2], C[0,2], C[2,0]
        err = (abs(vus-meas["Vus"])/meas["Vus"] + abs(vcb-meas["Vcb"])/meas["Vcb"]
               + abs(vub-meas["Vub"])/meas["Vub"] + abs(vtd-meas["Vtd"])/meas["Vtd"])
        if best is None or err < best[0]:
            best = (err, d, phi, vus, vcb, vub, vtd)
print(f"最佳: d={best[1]:.1f} φ={best[2]:.2f}")
print(f"  V_us={best[3]:.4f} (实测0.2253)  V_cb={best[4]:.4f} (实测0.0412)")
print(f"  V_ub={best[5]:.4f} (实测0.0038)  V_td={best[6]:.4f} (实测0.0089)")
