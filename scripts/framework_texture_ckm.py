# -*- coding: utf-8 -*-
"""
框架长出的质量矩阵 → 完整 CKM → V_cb 检验
结构（由三元互指 + η几何平均 + 动态残差推导，非假定）：
  M_ii = m_i（自耦合）
  M_11 = 0（最轻代自耦合为零：动态残差，最接近 0 基态）
  M_ij = √(m_i·m_j)（交叉耦合 = 几何平均：η 递归原则）
"""
import numpy as np

# 用户记分卡的质量谱
m_u, m_c, m_t = 2.16, 1263, 173950
m_d, m_s, m_b = 4.45, 95.9, 4271

def framework_matrix(m1, m2, m3, zero11=True):
    M = np.zeros((3, 3))
    M[0, 0] = 0.0 if zero11 else m1
    M[1, 1] = m2
    M[2, 2] = m3
    M[0, 1] = M[1, 0] = np.sqrt(m1 * m2)
    M[0, 2] = M[2, 0] = np.sqrt(m1 * m3)
    M[1, 2] = M[2, 1] = np.sqrt(m2 * m3)
    return M

def ckm_from(mat_u, mat_d):
    wu, Uu = np.linalg.eigh(mat_u)   # Uu 列 = 本征矢（升序质量）
    wd, Ud = np.linalg.eigh(mat_d)
    # 质量排序（升序 → 对应 (1,2,3) 代）
    CKM = Uu.T @ Ud
    return np.abs(CKM), wu, wd

print("=== 框架纹理（几何平均 + (1,1)零）完整 CKM ===\n")
M_u = framework_matrix(m_u, m_c, m_t)
M_d = framework_matrix(m_d, m_s, m_b)
CKM, wu, wd = ckm_from(M_u, M_d)

# 标准排列：CKM 行=(u,c,t)，列=(d,s,b)
print("质量（升序）:")
print(f"  上扇: {wu[0]:.2f}, {wu[1]:.1f}, {wu[2]:.1f}  (目标 2.16, 1263, 173950)")
print(f"  下扇: {wd[0]:.2f}, {wd[1]:.1f}, {wd[2]:.1f}  (目标 4.45, 95.9, 4271)")
print()
# 重排 CKM：行按 (u,c,t) 列按 (d,s,b) —— 本征矢已按质量升序，直接对应
print("|V| 矩阵（行=u,c,t；列=d,s,b）:")
for i in range(3):
    print("  " + "  ".join(f"{CKM[i,j]:.4f}" for j in range(3)))
print()
print("对照实测:")
print("  |V_us| = 0.2253   |V_cb| = 0.0412   |V_ub| = 0.0038")
print("  |V_td| = 0.0089   |V_ts| = 0.0400   |V_tb| ≈ 0.9991")
print()
# 提取（可能需要对角顺序）
# CKM[0,1] 应是 V_us（u→s），CKM[1,2] 是 V_cb（c→b）
print("框架预言:")
print(f"  V_us = {CKM[0,1]:.4f}  (实测 0.2253)")
print(f"  V_cb = {CKM[1,2]:.4f}  (实测 0.0412)")
print(f"  V_ub = {CKM[0,2]:.4f}  (实测 0.0038)")
print(f"  V_td = {CKM[2,0]:.4f}  (实测 0.0089)")

print("\n=== 对照：6-zero Fritzsch（文献已死）===")
def fritzsch(m1, m2, m3):
    M = np.zeros((3, 3))
    M[1, 1] = 0.0
    M[2, 2] = m3
    M[0, 1] = M[1, 0] = np.sqrt(m1 * m2)
    M[1, 2] = M[2, 1] = np.sqrt(m2 * m3)
    return M
M_uF = fritzsch(m_u, m_c, m_t)
M_dF = fritzsch(m_d, m_s, m_b)
CKMF, _, _ = ckm_from(M_uF, M_dF)
print(f"  V_us = {CKMF[0,1]:.4f}  V_cb = {CKMF[1,2]:.4f}  (文献: V_cb 被强制 ≥0.064)")
