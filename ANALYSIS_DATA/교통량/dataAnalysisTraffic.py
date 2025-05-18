import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
file_path = "C:/Users/GME-NOTE/Desktop/EDB_PJT/ANALYSIS_DATA/교통량/구별_교통량_포트홀_비교.csv"
df = pd.read_csv(file_path)

# 상관계수
corr = df['연평균_교통량_합계'].corr(df['포트홀_발생건수'])

# 시각화
plt.figure(figsize=(12, 8))
sns.regplot(
    data=df,
    x='연평균_교통량_합계',
    y='포트홀_발생건수',
    scatter_kws={'s': 70, 'color': 'skyblue'},
    line_kws={'color': 'red', 'linewidth': 2}
)

# 각 점에 자치구 이름 표시
for i in range(len(df)):
    plt.text(df['연평균_교통량_합계'][i],
             df['포트홀_발생건수'][i] + 50,
             df['구'][i],
             fontsize=9,
             ha='center')

# 상관계수 주석
plt.text(df['연평균_교통량_합계'].max() * 0.55,
         df['포트홀_발생건수'].max() * 0.9,
         f"상관계수(Pearson r): {corr:.2f}\n→ 교통량이 많은 구일수록 포트홀도 많음\n→ 유지보수 인력 우선 배치 필요",
         fontsize=12,
         bbox=dict(facecolor='white', edgecolor='black'))

# 제목 및 축 라벨
plt.title("교통량과 포트홀 발생의 관계 및 인력 배치 우선순위", fontsize=15)
plt.xlabel("연평균 교통량 합계")
plt.ylabel("포트홀 발생 건수")

plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
