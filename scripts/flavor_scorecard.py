# -*- coding: utf-8 -*-
# flavor_scorecard.py — S3/味对称族模型的数值预言记分卡（PDG 2024 数据）
import math, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=== S3/味对称族 预言记分卡 ===\n")

# --- 1. Gatto-Sartori-Tonin: sinθ_C ≈ √(m_d/m_s) ---
lam, lam_e = 0.2253, 0.0008          # V_us = sinθ_C, PDG
md, md_e = 4.67, 0.48                 # m_d(2GeV, MS-bar), PDG
ms, ms_e = 93.4, 8.6                  # m_s(2GeV, MS-bar), PDG
r = md/ms
r_e = r * math.sqrt((md_e/md)**2 + (ms_e/ms)**2)
sqrt_r = math.sqrt(r)
sqrt_r_e = 0.5 * sqrt_r / r * r_e
dev = (lam - sqrt_r)/sqrt_r*100
sigma = (lam - sqrt_r)/math.sqrt(lam_e**2 + sqrt_r_e**2)
print("1. Gatto-Sartori-Tonin: sinθ_C ≈ √(m_d/m_s)")
print(f"   sinθ_C = {lam} ± {lam_e}")
print(f"   √(m_d/m_s) = {sqrt_r:.4f} ± {sqrt_r_e:.4f}")
print(f"   偏差 {dev:.2f}%  ({abs(sigma):.1f}σ)")
print(f"   状态: 存活（但依赖质量方案，换跑动质量会漂到 1-3%）")

# --- 2. Koide: (√e+√μ+√τ)^2/(e+μ+τ) = 3/2 ---
me, mm, mt = 0.51099895000, 105.6583755, 1776.86
s = math.sqrt(me)+math.sqrt(mm)+math.sqrt(mt)
R = s*s/(me+mm+mt)
R_hi = (math.sqrt(me)+math.sqrt(mm)+math.sqrt(mt+0.12))**2/(me+mm+mt+0.12)
print("\n2. Koide 轻子公式")
print(f"   R = {R:.6f} vs 3/2, 偏差 {(R-1.5)/1.5*100:.4f}%  (δR≈{abs(R_hi-R):.2e})")
print("   状态: 存活，零自由参数，先验提出（1981）后验证")

# --- 3. 三双最大混合 TBM（A4/S4/S3 类模型的经典预言） ---
s12, s12e = 0.303, 0.012
s23, s23e = 0.451, 0.020
s13, s13e = 0.0222, 0.0006
print("\n3. 三双最大混合 TBM")
print(f"   sin²θ12 = 1/3 = 0.3333 vs 实测 {s12} → {(0.3333-s12)/s12e:.1f}σ")
print(f"   sin²θ23 = 1/2 = 0.5000 vs 实测 {s23} → {(0.5-s23)/s23e:.1f}σ")
print(f"   sin²θ13 = 0     vs 实测 {s13} → 死亡 {s13/s13e:.0f}σ")
print("   状态: 精确 TBM 已死（θ13≠0 在 2012 年 Daya Bay 杀死）")

# --- 4. 夸克轻子互补 QLC: θ_C + θ_12 ≈ 45° ---
thC = math.degrees(math.asin(lam))
th12 = math.degrees(math.asin(math.sqrt(s12)))
print("\n4. 夸克轻子互补: θ_C + θ12 ≈ 45°")
print(f"   {thC:.2f}° + {th12:.2f}° = {thC+th12:.2f}° vs 45° → 偏差 {(thC+th12-45)/45*100:.1f}%")
print("   状态: 已基本死亡")

print("\n=== 小结 ===")
print("S3/味对称族里活着的: GST (~0.8%, 方案敏感) 和 Koide (~0.001%, 干净)")
print("死掉的: 精确 TBM (θ13=0, 37σ)、夸克轻子互补 (3%)")
