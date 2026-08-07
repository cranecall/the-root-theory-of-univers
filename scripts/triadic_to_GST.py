# -*- coding: utf-8 -*-
"""三元互指 → 民主矩阵 → 破碎 → GST 推导验证"""
import math

md, ms = 4.67, 93.4   # MS-bar 2GeV
r = md / ms

# --- 民主矩阵（三元互指：三极等权互指，S3 对称） ---
# M0 = m0·J，J = 全1矩阵。本征值 (3m0, 0, 0)：一重两轻
J = [[1,1,1],[1,1,1],[1,1,1]]
print("民主矩阵 M0 = m0·J 本征值: (3m0, 0, 0) — 一重(第三代) + 两简并轻")
print("轻区本征矢: v1=(1,-1,0)/√2, v2=(1,1,-2)/√6\n")

# --- 破碎（回归不分裂不完全）：对角扰动 diag(e1,e2,e3) ---
# 轻区 2x2 投影
import numpy as np
def light_sector(e):
    v1 = np.array([1,-1,0])/math.sqrt(2)
    v2 = np.array([1,1,-2])/math.sqrt(6)
    P = np.diag(e)
    return np.array([[v1@P@v1, v1@P@v2],[v2@P@v1, v2@P@v2]])

# 情形A：纯对角破碎（残余 S2：A-B 交换）—— 给出 GST 纹理需要什么？
for e in [(0,0,1),(0.05,0.05,1)]:
    M = light_sector(e)
    print(f"对角破碎 {e}: 轻区矩阵 = {M}")

print()
# --- GST 纹理：[[0, √(md ms)], [√(md ms), ms]] —— 交叉项=几何平均 ---
a = math.sqrt(md*ms)
Mtex = np.array([[0, a],[a, ms]])
w, V = np.linalg.eigh(Mtex)
theta = math.atan2(V[1,0], V[0,0])
print(f"GST 纹理 [[0,√(md·ms)],[√(md·ms),ms]]:")
print(f"  本征值: {w[0]:.2f}, {w[1]:.2f}  MeV (应为 md, ms)")
print(f"  混合角 θ = {abs(theta)*180/math.pi:.2f}°  sinθ = {abs(math.sin(theta)):.4f}")
print(f"  GST 预言 sinθ=√(md/ms) = {math.sqrt(r):.4f}")
print(f"  实测 sinθ_C = 0.2253")
print(f"  纹理精确角偏差: {(abs(math.sin(theta))-0.2253)/0.2253*100:.1f}%")
print(f"  GST 近似偏差: {(math.sqrt(r)-0.2253)/0.2253*100:.2f}%")
print()
# Koide 确认
me, mm, mt = 0.51099895, 105.6583755, 1776.86
s = math.sqrt(me)+math.sqrt(mm)+math.sqrt(mt)
R = s*s/(me+mm+mt)
print(f"Koide R = {R:.6f} vs 3/2 → 偏差 {(R-1.5)/1.5*100:.4f}%")
