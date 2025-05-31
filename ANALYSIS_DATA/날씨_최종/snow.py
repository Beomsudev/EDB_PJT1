import pandas as pd
import matplotlib.pyplot as plt
import platform

# 한글 폰트 설정 (윈도우/맥/리눅스 대응)
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
else:
    plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_csv("제설시즌별_포트홀_제설제_통합.csv")

fig, ax1 = plt.subplots(figsize=(11,5))
ax2 = ax1.twinx()

# 포트홀 개수(합계) - 왼쪽 y축
ax1.plot(df["제설시즌"], df["포트홀_개수"], marker="o", color="tab:blue", label="포트홀 발생수(합계)")
ax1.set_ylabel("포트홀 발생수(합계)", color="tab:blue")
ax1.tick_params(axis='y', labelcolor="tab:blue")

# 제설제 사용량(톤) - 오른쪽 y축
ax2.plot(df["제설시즌"], df["제설제_사용량_톤"], marker="s", linestyle="--", color="tab:orange", label="제설제 사용량(톤)")
ax2.set_ylabel("제설제 사용량(톤)", color="tab:orange")
ax2.tick_params(axis='y', labelcolor="tab:orange")

plt.title("제설시즌별 제설제 사용량(톤)과 포트홀 발생수(합계)")
ax1.set_xlabel("제설시즌")
plt.xticks(rotation=30)
ax1.legend(loc="upper left")
ax2.legend(loc="upper right")
plt.tight_layout()
plt.savefig("05_제설시즌별_제설제_포트홀_비교.png", dpi=150, bbox_inches="tight")
plt.show()
