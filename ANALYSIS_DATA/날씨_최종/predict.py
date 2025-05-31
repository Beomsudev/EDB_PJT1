import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
else:
    plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 최근 5개년 데이터
data = {
    "연": [2020, 2021, 2022, 2023, 2024],
    "월 강수량(mm)": [139.6, 104.6, 393.8, 195.6, 115.9],
    "포트홀_개수":   [1555, 1963, 1418, 1543, 1191]
}
df = pd.DataFrame(data)

# 회귀 예측
X = df[["월 강수량(mm)"]].values
y = df["포트홀_개수"].values
model = LinearRegression().fit(X, y)

# 2025년 중앙값(148.6mm) 예측
rain_2025 = 148.6
potholes_2025 = int(model.predict(np.array([[rain_2025]]))[0])

# 예측 결과 합치기
df_plot = df.copy()
df_plot = pd.concat([df_plot, pd.DataFrame([{"연":2025, "월 강수량(mm)":rain_2025, "포트홀_개수":potholes_2025}])], ignore_index=True)

# 꺾은선 그래프
plt.figure(figsize=(10,5))
plt.plot(df_plot["연"], df_plot["포트홀_개수"], marker='o', label="실제/예측 포트홀 발생 수")
plt.plot(df_plot["연"], df_plot["월 강수량(mm)"], marker='s', linestyle='--', label="월 강수량(mm)", color='tab:blue', alpha=0.5)

plt.axvline(2024.5, color='gray', linestyle=':', label="2025년 예측구간")
plt.annotate(f'예측: {potholes_2025}건\n({rain_2025}mm)', xy=(2025, potholes_2025),
             xytext=(2025, potholes_2025+150),
             arrowprops=dict(arrowstyle="->", lw=1.2),
             fontsize=11, color="red", ha='center')

plt.xticks(df_plot["연"].astype(int))
plt.title("6월 월 강수량과 포트홀 발생 수 (2025년 예측 포함)")
plt.xlabel("연도")
plt.ylabel("포트홀 발생 수")
plt.legend()
plt.grid(True)
plt.tight_layout()

# ----- 저장! -----
plt.savefig("04_6월_강수량_포트홀_예측_그래프.png", dpi=150, bbox_inches="tight")
plt.show()
