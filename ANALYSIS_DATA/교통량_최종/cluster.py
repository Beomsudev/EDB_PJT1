import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import platform
from scipy.spatial import ConvexHull

# 폰트 설정
if platform.system() == "Windows":
    plt.rcParams["font.family"] = "Malgun Gothic"
else:
    plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_excel("교통량_최종_분석용_데이터.xlsx")
df['교통량_1000대당_포트홀'] = df['포트홀_발생건수'] / (df['연평균_교통량_합계'] / 1000)
df['도로연장_10km당_포트홀'] = df['포트홀_발생건수'] / (df['도로연장(Km)'] / 10)
df = df.replace([np.inf, -np.inf], np.nan)
df_clean = df[(df['연평균_교통량_합계'] > 0)].dropna()

vars_for_cluster = [
    '연평균_교통량_합계',
    '포트홀_발생건수',
    '구별예산_특별예산',
    '도로연장(Km)',
    '교통량_1000대당_포트홀',
    '도로연장_10km당_포트홀'
]
X = df_clean[vars_for_cluster].copy()
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 군집 수 고정
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=20)
clusters = kmeans.fit_predict(X_scaled)

# 결과 DataFrame
df_result = df_clean[['구']].copy()
df_result['cluster'] = clusters

# ===== 강제 군집 지정 =====
forced_labels = {
    '성북구': 1,   # 안정구 (관리 잘됨)
    '용산구': 2,   # 대규모 안정구
    # 필요시 원하는 구와 군집번호 추가
}
for gu, forced_cluster in forced_labels.items():
    idx = df_result[df_result['구'] == gu].index
    if len(idx) > 0:
        df_result.loc[idx, 'cluster'] = forced_cluster

# ===== 클러스터별 이름 네 해석 반영 =====
cluster_names = {
    0: "위험구 (교통량 많고 예산 부족, 예산↑ 필요)",
    1: "안정구 (교통량 적고 예상 적절, 관리 잘됨)",
    2: "안정구 (교통량 매우 많고 예산 매우 충분, 관리 잘됨)"
}
df_result['cluster_name'] = df_result['cluster'].map(cluster_names)

print("강제 지정+클러스터 이름 결과:\n", df_result)

# PCA 2D 변환
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# 색상 지정
colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple']

# 시각화 (군집 외곽선 추가)
plt.figure(figsize=(10,7))
for i in range(n_clusters):
    idx = df_result['cluster'] == i
    # 군집 점 찍기
    plt.scatter(X_pca[idx,0], X_pca[idx,1], label=f'{cluster_names[i]}', s=90, color=colors[i])
    # Convex Hull(군집 외곽선) 그리기 - 군집 점이 3개 이상일 때만
    if np.sum(idx) >= 3:
        points = np.vstack([X_pca[idx,0], X_pca[idx,1]]).T
        hull = ConvexHull(points)
        hull_points = points[hull.vertices]
        plt.plot(
            np.append(hull_points[:,0], hull_points[0,0]),
            np.append(hull_points[:,1], hull_points[0,1]),
            color=colors[i], lw=2, linestyle='-', alpha=0.7
        )
for i, name in enumerate(df_result['구'].values):
    plt.text(X_pca[i,0], X_pca[i,1], name, fontsize=9, ha='center', va='center', alpha=0.7)
plt.xlabel('PCA 1 (규모/교통량/예산 등)')
plt.ylabel('PCA 2 (위험/효율, 포트홀 비율 등)')
plt.title(f'서울시 구별 도로군집분석 (군집 수={n_clusters})')
plt.legend(fontsize=10)
plt.tight_layout()
plt.savefig('04_군집분석.png', dpi=200)
plt.close()
