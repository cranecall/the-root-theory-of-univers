# -*- coding: utf-8 -*-
"""
框架假设：下扇 (2,3) 耦合被 η/λ = 0.8443（2D/3D 投影保持率）抑制
纹理：[[0, a e^{iα}, d e^{iγ}], [a e^{-iα}, m2, c e^{iβ}], [d e^{-iγ}, c e^{-iβ}, m3]]
上扇：c_u = √(m_c·m_t)（几何平均，不抑制）
下扇：c_d = √(m_s·m_b)·(η/λ)（被 2D/3D 比率抑制）
扫相位，检验 V_cb 是否落入实测
"""
import numpy as np

ETA = (1 + np.sqrt(3)) / 2
LAM = (1 + np.sqrt(5)) / 2
RATIO = ETA / LAM   # 0.8443

m_u, m_c, m_t = 2.16, 1263, 173950
m_d, m_s, m_b = 4.45, 95.9, 4271
meas = {"Vus": 0.2253, "Vcb": 0.0412, "Vub": 0.0038, "Vtd": 0.0089}

print(f"η/λ = {RATIO:.4f}（框架 2D/3D 投影保持率）")
print(f"要求抑制因子 < 0.127/0.1495 = {0.127/0.1495:.4f}\n")

def tex(m1, m2, m3, alpha, beta, c_scale=1.0):
    a = np.sqrt(m1 * m2)
    c = np.sqrt(m2 * m3) * c_scale
    return np.array([
        [0.0, a*np.exp(1j*alpha), 0.0],
        [a*np.exp(-1j*alpha), m2, c*np.exp(1j*beta)],
        [0.0, c*np.exp(-1j*beta), m3],
    ])

def ckm_mag(Mu, Md):
    wu, Uu = np.linalg.eigh(Mu)
    wd, Ud = np.linalg.eigh(Md)
    return np.abs(Uu.conj().T @ Ud)

print("=== 下扇 (2,3) 被 η/λ 抑制 vs 不抑制 ===")
for label, c_scale in [("几何平均(不抑制)", 1.0), ("η/λ 抑制", RATIO)]:
    best = None
    for phi in np.linspace(0, np.pi, 121):
        Mu = tex(m_u, m_c, m_t, 0, 0)
        Md = tex(m_d, m_s, m_b, phi/2, phi/2, c_scale)
        C = ckm_mag(Mu, Md)
        vus, vcb, vub, vtd = C[0,1], C[1,2], C[0,2], C[2,0]
        err = (abs(vus-meas["Vus"])/meas["Vus"] + abs(vcb-meas["Vcb"])/meas["Vcb"]
               + abs(vub-meas["Vub"])/meas["Vub"] + abs(vtd-meas["Vtd"])/meas["Vtd"])
        if best is None or err < best[0]:
            best = (err, phi, vus, vcb, vub, vtd)
    print(f"\n{label}:")
    print(f"  最佳 φ={best[1]:.2f}: V_us={best[2]:.4f} V_cb={best[3]:.4f} V_ub={best[4]:.4f} V_td={best[5]:.4f}")
    print(f"  实测:               V_us=0.2253 V_cb=0.0412 V_ub=0.0038 V_td=0.0089")

print("\n=== 相对转动解析估计 ===")
th23u = np.sqrt(m_c/m_t)
th23d = np.sqrt(m_s/m_b)
th23d_s = np.sqrt(m_s/m_b) * RATIO
print(f"θ23^u = √(m_c/m_t) = {th23u:.4f}")
print(f"θ23^d = √(m_s/m_b) = {th23d:.4f} → V_cb ≈ {th23d-th23u:.4f}（不抑制）")
print(f"θ23^d = √(m_s/m_b)×(η/λ) = {th23d_s:.4f} → V_cb ≈ {th23d_s-th23u:.4f}（η/λ 抑制）")
print(f"实测 V_cb = 0.0412")
