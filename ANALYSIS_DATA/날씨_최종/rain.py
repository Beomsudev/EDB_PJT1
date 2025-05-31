import pandas as pd
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
else:
    plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_csv("./포트홀_날씨_최종분석용.csv")

# 6~8월 데이터만 필터
summer = df[df["월"].isin([6, 7, 8])]

# 연도별 6~8월 강수량/포트홀 발생 합계 집계
summer_grouped = summer.groupby("연").agg({
    "일강수량(mm)": "sum",
    "포트홀_개수": "sum"
}).reset_index()

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(12, 6))

# 강수량(좌측 y축, 파란선)
ax1.plot(
    summer_grouped["연"], summer_grouped["일강수량(mm)"],
    "o-", color="blue", label="강수량(6~8월 합계)"
)
ax1.set_ylabel("강수량(6~8월 합계, mm)", color="blue", fontsize=14)
ax1.tick_params(axis="y", labelcolor="blue")
ax1.set_xlabel("연도", fontsize=14)

# 포트홀 발생수(우측 y축, 빨간선)
ax2 = ax1.twinx()
ax2.plot(
    summer_grouped["연"], summer_grouped["포트홀_개수"],
    "s--", color="red", label="포트홀 발생(6~8월 합계)"
)
ax2.set_ylabel("포트홀 발생(6~8월 합계)", color="red", fontsize=14)
ax2.tick_params(axis="y", labelcolor="red")

# 타이틀, 범례
plt.title("연도별 6~8월 강수량과 포트홀 발생 꺾은선그래프", fontsize=17)
ax1.legend(loc="upper left", fontsize=13)
ax2.legend(loc="upper right", fontsize=13)

plt.tight_layout()
plt.savefig("02_6~8월_강수량_포트홀_연도별_꺾은선그래프.png", dpi=300)
plt.show()
