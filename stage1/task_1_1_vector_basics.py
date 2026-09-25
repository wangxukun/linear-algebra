# -*- coding: utf-8 -*-
"""
Stage 1 · 任务 1.1 向量的本质 —— 可视化演示（理论讲义见 stage1/notes/）

图 1  三维向量加法：u、w 同起点画出，平移副本（虚线）呈现三角形法则
      （首尾相接）与平行四边形法则（对角线 = u+w）。
图 2  数乘 k·v：k = -1, 1/2, 1, 2 四支箭头全部落在过原点的同一条直线上
      —— "数乘出直线"（Stage 1.3/1.4 的种子）。

运行：python stage1/task_1_1_vector_basics.py
产出：控制台数值验证 + stage1/fig_1_1_addition_3d.png
                  + stage1/fig_1_1_scalar_mult_3d.png
"""
import math
import os

import matplotlib

matplotlib.use("Agg")  # 无显示环境直接出图到文件
import matplotlib.pyplot as plt

# Windows 中文字体
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

HERE = os.path.dirname(os.path.abspath(__file__))


# ---------- 只用本讲学过的工具 ----------
def norm(v):
    """模长 ‖v‖ = √(v₁²+…+vₙ²)，讲义 §2 公式的直接实现"""
    return math.sqrt(sum(x * x for x in v))


def unit(v):
    """单位向量 v̂ = v/‖v‖，讲义 §3"""
    n = norm(v)
    return tuple(x / n for x in v)


def add(a, b):
    """向量加法：对应分量相加，讲义 §4"""
    return tuple(a[i] + b[i] for i in range(len(a)))


def scale(k, v):
    """数乘：k·v = (k·v₁, k·v₂, …)，讲义 §5"""
    return tuple(k * x for x in v)


# ---------- 第一部分：把自检题 Q2 的手算交给程序复核 ----------
u = (2, -1, 3)
w = (0, 4, -2)
u_plus_w = add(u, w)                              # 期望 (2, 3, 1)
two_u_minus_w = add(scale(2, u), scale(-1, w))    # 减法 = 加负向量，期望 (4, -6, 8)

print("=" * 60)
print("自检题 Q2：手算 vs 程序复核")
print(f"  u + w   = {u_plus_w}          （你算的 (2, 3, 1)）")
print(f"  2u - w  = {two_u_minus_w}     （你算的 (4, -6, 8)）")
print(f"  ‖u + w‖ = √14 ≈ {norm(u_plus_w):.4f}   （你算的 √14）")
assert u_plus_w == (2, 3, 1)
assert two_u_minus_w == (4, -6, 8)
assert abs(norm(u_plus_w) - math.sqrt(14)) < 1e-12

# 讲义 §3/§5 性质的数值检验
v = (1, 2, 2)  # ‖v‖ = 3，数字干净
v_hat = unit(v)
print(f"\n性质检验（v = {v}，‖v‖ = {norm(v):.0f}）")
print(f"  v̂ = {tuple(round(x, 6) for x in v_hat)}，‖v̂‖ = {norm(v_hat):.12f}")
assert abs(norm(v_hat) - 1.0) < 1e-12
for k in (-1, 0.5, 2):
    lhs, rhs = norm(scale(k, v)), abs(k) * norm(v)
    ok = abs(lhs - rhs) < 1e-12
    print(f"  k = {k:>4}:  ‖k·v‖ = {lhs:.6f}，|k|·‖v‖ = {rhs:.6f}，一致: {ok}")
    assert ok
print("全部断言通过 ✓")


# ---------- 绘图工具 ----------
def setup_axes(ax, pts, title, elev=18, azim=35):
    """三轴统一范围 + 等比例盒，保证 3D 箭头几何不变形"""
    pts = __import__("numpy").array(pts)
    lo, hi = pts.min(axis=0), pts.max(axis=0)
    mid, half = (lo + hi) / 2, (hi - lo).max() / 2 + 1.0
    ax.set_xlim(mid[0] - half, mid[0] + half)
    ax.set_ylim(mid[1] - half, mid[1] + half)
    ax.set_zlim(mid[2] - half, mid[2] + half)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlabel("x"), ax.set_ylabel("y"), ax.set_zlabel("z")
    ax.set_title(title, fontsize=11)


def draw_arrow(ax, vec, color, origin=(0, 0, 0), lw=2.4, ls="-"):
    ax.quiver(*origin, *vec, color=color, linewidth=lw,
              arrow_length_ratio=0.09, linestyle=ls)


def mark_point(ax, p, text, dx=0.12, dy=0.12, dz=0.15):
    ax.scatter(*p, color="black", s=16)
    ax.text(p[0] + dx, p[1] + dy, p[2] + dz, text, fontsize=9)


# ---------- 图 1：三维向量加法（三角形 + 平行四边形法则） ----------
fig = plt.figure(figsize=(8.5, 7))
ax = fig.add_subplot(111, projection="3d")

draw_arrow(ax, u, "tab:blue")                   # u 从原点出发
draw_arrow(ax, w, "tab:orange")                 # w 从原点出发
draw_arrow(ax, u_plus_w, "crimson", lw=3.2)     # 合向量：加粗
draw_arrow(ax, w, "tab:orange", origin=u, lw=1.6, ls="--")  # w 平移到 u 的头 → 三角形法则
draw_arrow(ax, u, "tab:blue", origin=w, lw=1.6, ls="--")    # u 平移到 w 的头 → 补成平行四边形

mark_point(ax, (0, 0, 0), "O（原点）")
mark_point(ax, u, "u 的头")
mark_point(ax, w, "w 的头")
mark_point(ax, u_plus_w, "u+w 的头", dx=0.15, dy=0.2, dz=0.1)

setup_axes(ax, [(0, 0, 0), u, w, u_plus_w],
           "向量加法 u + w = (2, 3, 1)\n"
           "实线 = u、w、u+w；虚线 = 平移副本（首尾相接成三角形，同起点补成平行四边形）")
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_1_1_addition_3d.png"), dpi=150)
print("已保存 fig_1_1_addition_3d.png")

# ---------- 图 2：数乘 k·v —— "数乘出直线" ----------
fig = plt.figure(figsize=(8.5, 7))
ax = fig.add_subplot(111, projection="3d")

# 共线的箭头互相遮挡：从最长画到最短，短箭头叠画在长箭头之上，
# 形成"嵌套色段"（青 O→½v，紫 ½v→v，红 v→2v），共线且比例一目了然
cases = [(2, "k=2（拉长）", "tab:red", 2.0),
         (1, "k=1（v 本尊）", "tab:purple", 3.0),
         (0.5, "k=0.5（缩短）", "tab:cyan", 3.6),
         (-1, "k=-1（反向）", "tab:green", 2.4)]
for k, label, color, lw in cases:
    draw_arrow(ax, scale(k, v), color, lw=lw)
for k, label, color, lw in cases:
    tip = scale(k, v)
    ax.text(tip[0] + 0.12, tip[1] + 0.12, tip[2] + 0.15, label,
            color=color, fontsize=10, fontweight="bold")

# 过原点的直线：所有 k·v 的宿命 —— Stage 1.3 将称之为 span{v}
import numpy as np

t = np.linspace(-1.3, 2.3, 20)
ax.plot(t * v[0], t * v[1], t * v[2], "k--", linewidth=1.1, alpha=0.55)
ax.text(2.3 * v[0] + 0.1, 2.3 * v[1], 2.3 * v[2],
        "过原点的直线（span{v}）", fontsize=9, alpha=0.8)

mark_point(ax, (0, 0, 0), "O（原点）")
setup_axes(ax, [(0, 0, 0)] + [scale(k, v) for k, *_ in cases],
           "数乘 k·v：所有倍数共线 —— k>0 同侧伸缩，k<0 翻到反向\n"
           "黑色虚线 = v 的方向所在直线（过原点）",
           elev=15, azim=40)
fig.tight_layout()
fig.savefig(os.path.join(HERE, "fig_1_1_scalar_mult_3d.png"), dpi=150)
print("已保存 fig_1_1_scalar_mult_3d.png")
