import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 한글 폰트 설정 (Windows/Mac)
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
else:
    plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 로드
df = pd.read_csv("../날씨_최종/포트홀_날씨_분석용.csv")

# 1. 결측치 50% 이상 컬럼 제거
threshold = len(df) * 0.5
drop_cols = [col for col in df.columns if df[col].isnull().sum() > threshold]
df2 = df.drop(columns=drop_cols)

# 2. 숫자형 컬럼만 평균으로 결측치 채움
num_cols = df2.select_dtypes(include="number").columns
df2[num_cols] = df2[num_cols].fillna(df2[num_cols].mean())

# ---------------------------
# 1. 임계치(Threshold) 분석
# ---------------------------
# 일강수량 30mm 기준으로 분류
df2["강수_30mm이상"] = df2["일강수량(mm)"] >= 30

# 30mm 이상/미만 포트홀 개수 평균
mean_above_30 = df2.loc[df2["강수_30mm이상"], "포트홀_개수"].mean()
mean_below_30 = df2.loc[~df2["강수_30mm이상"], "포트홀_개수"].mean()
print(f"[임계치 분석] 일강수량 30mm 이상: 평균 {mean_above_30:.1f}개, 미만: 평균 {mean_below_30:.1f}개")

# 50mm 이상 존재 여부 확인 및 평균
if (df2["일강수량(mm)"] >= 50).sum() > 0:
    mean_above_50 = df2.loc[df2["일강수량(mm)"] >= 50, "포트홀_개수"].mean()
    print(f"일강수량 50mm 이상: 평균 {mean_above_50:.1f}개")
else:
    print("일강수량 50mm 이상인 월이 없습니다.")

# Boxplot 시각화
plt.figure(figsize=(5, 5))
sns.boxplot(x="강수_30mm이상", y="포트홀_개수", data=df2)
plt.xticks([0, 1], ["<30mm", "≥30mm"])
plt.title("일강수량 30mm 이상/미만의 포트홀 발생 분포")
plt.show()

# ---------------------------
# 2. RandomForest 변수 중요도
# ---------------------------
from sklearn.ensemble import RandomForestRegressor

# 독립변수/종속변수 설정
X = df2.drop(columns=["연월", "포트홀_개수", "포트홀_면적"], errors='ignore')
y = df2["포트홀_개수"]

# 랜덤포레스트 회귀 모델
model = RandomForestRegressor(n_estimators=300, random_state=42)
model.fit(X, y)

importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(8, 7))
sns.barplot(y=X.columns[indices], x=importances[indices], orient='h')
plt.title("RandomForest 변수 중요도")
plt.xlabel("중요도")
plt.tight_layout()
plt.show()

print("\n[RandomForest 변수 중요도 TOP5]")
for i in indices[:5]:
    print(f"{X.columns[i]}: {importances[i]:.3f}")

# ---------------------------
# 3. 군집분석 (KMeans)
# ---------------------------
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

clu_vars = X.columns.tolist()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df2[clu_vars])

kmeans = KMeans(n_clusters=2, random_state=42, n_init=20)
clusters = kmeans.fit_predict(X_scaled)
df2["포트홀_군집"] = clusters

# 군집별 포트홀 개수 통계
print("\n[군집별 포트홀 개수 통계]")
print(df2.groupby("포트홀_군집")["포트홀_개수"].describe())

# 군집별 주요 변수 평균
print("\n[군집별 주요 변수 평균]")
print(df2.groupby("포트홀_군집")[clu_vars].mean())

# 군집별 boxplot
plt.figure(figsize=(5,5))
sns.boxplot(x="포트홀_군집", y="포트홀_개수", data=df2)
plt.title("군집별 포트홀 개수 분포")
plt.show()
