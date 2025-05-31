import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 한글 폰트 설정
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
else:
    plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_csv("./포트홀_날씨_최종분석용.csv")

# 분석에 쓸 컬럼만 추출 (연, 월, 등 불필요한 컬럼 제외)
cols = [c for c in df.columns if c not in ["연", "월"]]
corr = df[cols].corr(numeric_only=True)
corr_pothole = corr[["포트홀_개수"]].sort_values("포트홀_개수", ascending=False)

plt.figure(figsize=(5, 8))
sns.heatmap(
    corr_pothole,
    annot=True, fmt=".2f", cmap="coolwarm",
    cbar=True, vmin=-1, vmax=1, annot_kws={"size": 12}
)
plt.title("포트홀 개수와 월별 기상 변수 상관계수", fontsize=14)
plt.yticks(fontsize=11)
plt.xticks(fontsize=11)
plt.tight_layout()
plt.savefig("01_포트홀_상관계수_히트맵_최종_연월제외.png", dpi=300)
plt.show()
