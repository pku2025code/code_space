import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# 1. 定义模拟参数
N_SIM = 500000  # 模拟次数（样本量）
THRESHOLD = -1.535  # 违约阈值
RHO_VALUES = np.linspace(0.05, 0.95, 19)  # ρ的取值范围 (0.05, 0.10, ..., 0.95)
R_RHO_ESTIMATES = []  # 存储R(ρ)的估计值

# 2. 计算边缘违约概率 P_D
# P_D = P(Ri < THRESHOLD) = Phi(THRESHOLD)
P_D = norm.cdf(THRESHOLD)

# 3. 循环遍历每个 ρ 值进行模拟
for rho in RHO_VALUES:
    # --- a. 生成二维正态随机数 ---
    # 构建协方差矩阵 Sigma
    Sigma = np.array([[1, rho], [rho, 1]])

    # 使用 Cholesky 分解生成相关正态随机数
    L = np.linalg.cholesky(Sigma)
    Z = np.random.normal(0, 1, size=(2, N_SIM))

    # R 是二维正态分布的随机向量 (R1, R2)
    R = L @ Z  # 矩阵乘法

    R1 = R[0, :]
    R2 = R[1, :]

    # --- b. 计算示性算子 d1 和 d2 ---
    # d_i = I{R_i < THRESHOLD}
    d1 = (R1 < THRESHOLD).astype(int)
    d2 = (R2 < THRESHOLD).astype(int)

    # --- c. 计算相关系数 R(ρ) 的估计值 ---
    # 使用解析公式: R(ρ) = (E[d1*d2] - P_D^2) / (P_D * (1 - P_D))

    # 估计 E[d1*d2] = P(R1 < THRESHOLD, R2 < THRESHOLD)
    P_12_est = np.mean(d1 * d2)

    # 估计 R(ρ)
    # 分母 Var(d) = P_D * (1 - P_D)
    # 分子 Cov(d1, d2) = P_12_est - P_D^2
    if P_D * (1 - P_D) > 1e-10:  # 避免除以零
        R_rho_est = (P_12_est - P_D ** 2) / (P_D * (1 - P_D))
    else:
        # 当P_D接近0或1时，相关系数接近未定义，但对于本例不会发生。
        R_rho_est = 0

    R_RHO_ESTIMATES.append(R_rho_est)

# 4. 绘制曲线
plt.figure(figsize=(10, 6))
plt.plot(RHO_VALUES, R_RHO_ESTIMATES, marker='o', linestyle='-', color='blue', label='$R(\\rho)$ Estimated')
plt.title(f'Function $R(\\rho)$ via Monte Carlo Simulation (N={N_SIM:,})')
plt.xlabel('Original Correlation $\\rho = \\text{Corr}(R_1, R_2)$')
plt.ylabel('Indicator Correlation $R(\\rho) = \\text{Corr}(d_1, d_2)$')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()

# 5. 打印部分结果 (可选)
print("--- 模拟结果摘要 ---")
print(f"阈值: {THRESHOLD}")
print(f"边缘违约概率 P_D: {P_D:.4f}")
print("  ρ    |  R(ρ) Estimate")
print("-------|----------------")
for rho, R_rho in zip(RHO_VALUES[::4], R_RHO_ESTIMATES[::4]):
    print(f"{rho:.2f}  |   {R_rho:.4f}")