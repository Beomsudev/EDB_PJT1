import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform

# 한글 폰트 설정 (Windows 기준: 맑은 고딕)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='AppleGothic')  # macOS 등

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

# CSV 불러오기
df = pd.read_csv("포트홀_날씨_통합.csv")

# 수치형 열만 추출
numeric_df = df.select_dtypes(include='number')
corr_matrix = numeric_df.corr()

# 포트홀 관련 변수와만 상관관계 추출
target_col = '포트홀_개수'
corr_target = corr_matrix[[target_col]].sort_values(by=target_col, ascending=False)

# 히트맵 그리기
plt.figure(figsize=(5, 12))
sns.heatmap(corr_target, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title(f"{target_col}와 다른 변수 간 상관관계")
plt.tight_layout()
plt.show()
