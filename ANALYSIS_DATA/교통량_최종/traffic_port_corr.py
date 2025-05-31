import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from scipy.stats import pearsonr
from sklearn.preprocessing import MinMaxScaler
import os

# 한글 폰트 설정
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 저장 폴더 생성
output_dir = "../교통량_최종/포트홀_분석_그래프"
os.makedirs(output_dir, exist_ok=True)

# 데이터 불러오기
df = pd.read_excel("C:/Users/GME-NOTE/Desktop/1/EDB/EDB_PJT/ANALYSIS_DATA/교통량_최종/교통량_최종_분석용_데이터.xlsx", sheet_name="Sheet1")
df_sorted = df.sort_values("포트홀_발생건수", ascending=False)

# ▣ 1. 산점도 + 회귀선 + 상관계수
x = df["연평균_교통량_합계"]
y = df["포트홀_발생건수"]
r, _ = pearsonr(x, y)
plt.figure(figsize=(10, 7))
sns.regplot(x=x, y=y, scatter_kws={'s': 60}, line_kws={'color': 'red'})
for i in range(len(df)):
    plt.text(x[i], y[i], df["구"][i], fontsize=9, ha='left', va='bottom')
plt.title(f"포트홀 발생건수 vs 연평균 교통량 (상관계수 r = {r:.2f})")
plt.xlabel("연평균 교통량 합계")
plt.ylabel("포트홀 발생건수")
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01_산점도_회귀선.png"))
plt.close()

# ▣ 2. 막대 + 꺾은선 그래프 (포트홀 + 교통량)
fig, ax1 = plt.subplots(figsize=(12, 6))
ax1.bar(df_sorted["구"], df_sorted["포트홀_발생건수"], color='salmon')
ax1.set_xlabel("구 (포트홀 발생순 정렬)")
ax1.set_ylabel("포트홀 발생건수", color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.set_xticks(range(len(df_sorted)))
ax1.set_xticklabels(df_sorted["구"], rotation=45)
ax2 = ax1.twinx()
ax2.plot(df_sorted["구"], df_sorted["연평균_교통량_합계"], color='blue', marker='o')
ax2.set_ylabel("연평균 교통량", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')
plt.title("포트홀 발생수(막대) & 교통량(꺾은선) 비교")
fig.tight_layout()
plt.savefig(os.path.join(output_dir, "02_포트홀_교통량_비교.png"))
plt.close()

# ▣ 3. 정규화된 예산 + 교통량
scaler = MinMaxScaler()
normalized = scaler.fit_transform(df_sorted[["구별예산_특별예산", "연평균_교통량_합계"]])
df_sorted["예산_정규화"] = normalized[:, 0]
df_sorted["교통량_정규화"] = normalized[:, 1]
fig, ax1 = plt.subplots(figsize=(14, 7))
ax1.bar(df_sorted["구"], df_sorted["포트홀_발생건수"], color='salmon')
ax1.set_ylabel("포트홀 발생건수", color='red')
ax1.tick_params(axis='y', labelcolor='red')
ax1.set_xticks(range(len(df_sorted)))
ax1.set_xticklabels(df_sorted["구"], rotation=45)
ax2 = ax1.twinx()
ax2.plot(df_sorted["구"], df_sorted["예산_정규화"], color='green', marker='o')
ax2.plot(df_sorted["구"], df_sorted["교통량_정규화"], color='blue', marker='s')
ax2.set_ylabel("정규화된 예산 / 교통량", color='black')
ax2.tick_params(axis='y', labelcolor='black')
fig.legend(["포트홀 발생건수", "구별 예산(정규화)", "연평균 교통량(정규화)"],
           loc='upper right', bbox_to_anchor=(0.98, 0.94), ncol=1, fontsize=10)
plt.title("포트홀 발생(막대) + 예산/교통량(정규화 꺾은선)", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig(os.path.join(output_dir, "03_정규화_비교.png"))
plt.close()

# ▣ 4. 상위/하위 5개 구 비교
# 데이터 정렬
df_sorted = df.sort_values("포트홀_발생건수", ascending=False)

# 상위/하위 3개 구 추출 및 정규화
df_top3 = df_sorted.head(3).copy()
df_bottom3 = df_sorted.tail(3).copy()

df_top3[["예산_정규화", "교통량_정규화"]] = MinMaxScaler().fit_transform(df_top3[["구별예산_특별예산", "연평균_교통량_합계"]])
df_bottom3[["예산_정규화", "교통량_정규화"]] = MinMaxScaler().fit_transform(df_bottom3[["구별예산_특별예산", "연평균_교통량_합계"]])

# 그래프
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12), sharex=True)

# ▶ 상위 3개 구
bar1 = ax1.bar(df_top3["구"], df_top3["포트홀_발생건수"], color='salmon')
ax3 = ax1.twinx()
line1, = ax3.plot(df_top3["구"], df_top3["교통량_정규화"], color='blue', marker='s')
line2, = ax3.plot(df_top3["구"], df_top3["예산_정규화"], color='green', marker='o')

# ▶ 하위 3개 구
bar2 = ax2.bar(df_bottom3["구"], df_bottom3["포트홀_발생건수"], color='salmon')
ax4 = ax2.twinx()
line3, = ax4.plot(df_bottom3["구"], df_bottom3["교통량_정규화"], color='blue', marker='s')
line4, = ax4.plot(df_bottom3["구"], df_bottom3["예산_정규화"], color='green', marker='o')

# 정확한 객체 순서로 범례 설정
fig.legend([line1, line2, bar1], ["연평균 교통량(정규화)", "구별 예산(정규화)", "포트홀 발생건수"],
           loc='upper right', bbox_to_anchor=(0.98, 0.94), fontsize=10)


# 제목 및 저장
plt.suptitle("포트홀 발생 상/하위 3개 구 비교 (막대 + 정규화 꺾은선)", fontsize=14)
plt.tight_layout(rect=[0, 0.03, 1, 0.90])
plt.savefig(os.path.join(output_dir, "04_상하위3_정규화_비교.png"))
plt.close()