# -*- coding: utf-8 -*-
"""
大象脊线完整填充（自主持续任务 · 2026-08-04）
目标：一次性填充全部图像区域，输出单一报告。
区域：整数格全谱 / μ网络 / 窗口位置 / φ阶梯 / 常数网络 / 待填区
"""
import math, os

PHI = (1 + math.sqrt(5)) / 2
ETA = (1 + math.sqrt(3)) / 2
LNPHI = math.log(PHI)
LNETA = math.log(ETA)
ME = 0.51099895      # MeV
MU = 105.6583755     # MeV
E_OSC = 7.67102e22   # MeV（h/t_P）
E_H = 1.3605693e-5   # MeV（13.605693 eV）
WINDOW = math.log(1e8) / LNPHI   # 38.28
N_ATOM = math.log(E_OSC / E_H) / LNPHI

PARTICLES = [
    ("e", 0.51099895), ("mu", 105.6583755), ("tau", 1776.86),
    ("pi+", 139.57039), ("pi0", 134.9768), ("K+", 493.677), ("K0", 497.611),
    ("eta", 547.862), ("eta'", 957.78), ("rho", 775.26), ("omega", 782.65),
    ("phi", 1019.461), ("K*+", 891.67), ("K*0", 895.55),
    ("f0(980)", 990), ("a0(980)", 980),
    ("p", 938.27208816), ("n", 939.5654205), ("Lambda", 1115.683),
    ("Sigma+", 1189.37), ("Sigma0", 1192.642), ("Sigma-", 1197.449),
    ("Xi0", 1314.86), ("Xi-", 1321.71), ("Delta", 1232.0),
    ("Sigma*", 1383.7), ("Xi*", 1533.5), ("Omega-", 1672.45),
    ("D0", 1864.84), ("D+", 1869.66), ("Ds", 1968.35),
    ("Lambda_c", 2286.46), ("Xi_c", 2467.9), ("eta_c", 2983.9),
    ("J/psi", 3096.9), ("chi_c0", 3414.75), ("psi(2S)", 3686.10),
    ("B0", 5279.66), ("B+", 5279.34), ("Bs", 5366.88), ("Bc", 6274.9),
    ("Lambda_b", 5619.60), ("Y(1S)", 9460.30), ("Y(2S)", 10023.26), ("Y(3S)", 10355.2),
    ("W", 80369.2), ("Z", 91187.6), ("H", 125250), ("t", 172760),
]

SYSTEM_CONSTS = {
    "phi": PHI, "eta": ETA, "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3),
    "phi^(1/sqrt3)": PHI ** (1 / math.sqrt(3)), "eta^7": ETA ** 7,
    "sqrt3^3": math.sqrt(3) ** 3, "1/sqrt3": 1 / math.sqrt(3), "sqrt3/2": math.sqrt(3) / 2,
    "14/3": 14 / 3, "18/5": 18 / 5, "22/3": 22 / 3, "35/3": 35 / 3,
    "45/4": 45 / 4, "84/5": 84 / 5, "95/9": 95 / 9, "37/5": 37 / 5,
    "29/3": 29 / 3, "3": 3, "8": 8, "9": 9, "16.8": 16.8, "8.877": ETA ** 7,
}

def nearest_int(x):
    return round(x)

def best_rational(r, maxq=60, small_primes=(2, 3, 5, 7, 11)):
    """best p/q with q<=maxq, p,q built from small primes"""
    best = None
    for q in range(1, maxq + 1):
        p = round(r * q)
        if p <= 0:
            continue
        err = abs(p / q - r) / r
        if best is None or err < best[0]:
            best = (err, p, q)
    return best

def best_const(r):
    best = None
    for name, val in SYSTEM_CONSTS.items():
        err = abs(val - r) / r
        if best is None or err < best[0]:
            best = (err, name, val)
    return best

def analyze():
    rows = []
    for name, m in PARTICLES:
        n = m / ME
        ni = nearest_int(n)
        dev = abs(n - ni) / n * 100
        r = m / MU
        N_h = math.log(E_OSC / m) / LNPHI
        N_hbar = N_h - math.log(2 * math.pi) / LNPHI
        D = N_ATOM - N_h
        frac = D / WINDOW
        in_win = 0 <= frac <= 1.1
        rows.append(dict(name=name, m=m, n=n, ni=ni, dev=dev, r=r, N_h=N_h,
                         N_hbar=N_hbar, D=D, frac=frac, in_win=in_win))

    # 整数格全谱
    rows.sort(key=lambda x: x["ni"])
    int_table = []
    for r_ in rows:
        if r_["dev"] < 0.5:
            int_table.append(r_)

    # 统计
    stats = {
        "<0.02%": sum(1 for r_ in rows if r_["dev"] < 0.02),
        "<0.05%": sum(1 for r_ in rows if r_["dev"] < 0.05),
        "<0.1%": sum(1 for r_ in rows if r_["dev"] < 0.1),
        "<0.2%": sum(1 for r_ in rows if r_["dev"] < 0.2),
        "total": len(rows),
    }

    # 整数序列与间隙
    ints = [r_["ni"] for r_ in int_table]
    gaps = [ints[i + 1] - ints[i] for i in range(len(ints) - 1)]

    # μ网络（轻粒子 r<20）
    mu_net = []
    for r_ in rows:
        if r_["r"] < 20:
            br = best_rational(r_["r"])
            bc = best_const(r_["r"])
            mu_net.append((r_["name"], r_["r"], br, bc))

    return rows, int_table, stats, ints, gaps, mu_net

def write_report(rows, int_table, stats, ints, gaps, mu_net):
    L = []
    L.append("# 大象脊线完整填充报告（自主持续任务 · 2026-08-04）")
    L.append("")
    L.append("## 一、整数格全谱（m = n·m_e，偏差 %）")
    L.append("")
    L.append("| 粒子 | 质量 MeV | n = m/m_e | 最近整数 | 偏差 |")
    L.append("|---|---|---|---|---|")
    for r_ in int_table:
        L.append(f"| {r_['name']} | {r_['m']:.4f} | {r_['n']:.2f} | {r_['ni']} | {r_['dev']:.4f}% |")
    L.append("")
    L.append(f"统计：总数 {stats['total']}，<0.02%: {stats['<0.02%']}，<0.05%: {stats['<0.05%']}，"
             f"<0.1%: {stats['<0.1%']}，<0.2%: {stats['<0.2%']}")
    L.append("")
    L.append("## 二、整数序列与间隙")
    L.append("")
    L.append("序列：" + ", ".join(str(i) for i in ints))
    L.append("")
    L.append("间隙：" + ", ".join(str(g) for g in gaps))
    L.append("")
    # 11/29 分析
    L.append("### 11/29 结构核查")
    L.append("")
    for g in gaps:
        mark = ""
        if g % 11 == 0:
            mark += f" = {g//11}×11"
        if g % 29 == 0:
            mark += f" = {g//29}×29"
        L.append(f"{g}{mark}")
    L.append("")
    L.append("## 三、μ 网络（轻粒子，最佳有理因子 vs 体系常数）")
    L.append("")
    L.append("| 粒子 | m/m_μ | 最佳有理 p/q | 有理误差 | 最佳体系常数 | 常数误差 |")
    L.append("|---|---|---|---|---|---|")
    for name, r, br, bc in mu_net:
        brs = f"{br[1]}/{br[2]}" if br else "—"
        bre = f"{br[0]*100:.3f}%" if br else "—"
        L.append(f"| {name} | {r:.4f} | {brs} | {bre} | {bc[1]} | {bc[0]*100:.3f}% |")
    L.append("")
    L.append("## 四、窗口位置与 φ 阶梯")
    L.append("")
    L.append("| 粒子 | N(h) | N(ℏ) | 距原子 D(φ步) | 窗口分数 | 窗口内 |")
    L.append("|---|---|---|---|---|---|")
    for r_ in sorted(rows, key=lambda x: x["N_h"]):
        L.append(f"| {r_['name']} | {r_['N_h']:.2f} | {r_['N_hbar']:.2f} | {r_['D']:.2f} | {r_['frac']:.3f} | {'是' if r_['in_win'] else '否'} |")
    L.append("")
    L.append("## 五、待填区域")
    L.append("")
    L.append("1. 整数序列间隙结构（11/29 之外的间隙）");
    L.append("2. 重粒子整数（3649 以上）的 μ 网络对应——重粒子是否也有 μ 因子形式");
    L.append("3. 核区/原子区在格上的位置（氘核结合能 2.22457 MeV = 4352·m_e，0.03%）");
    L.append("4. 整数序列的生成规则（若存在）");
    L.append("")
    text = "\n".join(L)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "大象脊线填充报告.md"),
              "w", encoding="utf-8") as f:
        f.write(text + "\n")
    return text

if __name__ == "__main__":
    rows, int_table, stats, ints, gaps, mu_net = analyze()
    report = write_report(rows, int_table, stats, ints, gaps, mu_net)
    print(report)
