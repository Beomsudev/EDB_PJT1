import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import platform

# ✅ 한글 폰트 설정 (Windows: 맑은 고딕)
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
path = r"C:\Users\GME-NOTE\Desktop\EDB_PJT\ANALYSIS_DATA\날씨\포트홀_제설제_통합_시즌별.csv"
df = pd.read_csv(path)

# 회귀선 포함 산점도 (sns.regplot 사용)
plt.figure(figsize=(8, 6))
sns.regplot(data=df, x='사용량(톤)', y='합계', ci=None)
plt.xlabel('제설제 사용량 (톤)')
plt.ylabel('포트홀 발생 합계')
plt.title('제설제 사용량과 포트홀 발생 합계의 선형 관계')
plt.grid(True)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import platform

# ✅ 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
else:
    plt.rc('font', family='AppleGothic')

plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
path = r"C:\Users\GME-NOTE\Desktop\EDB_PJT\ANALYSIS_DATA\날씨\포트홀_제설제_통합_시즌별.csv"
df = pd.read_csv(path)

# 제설시즌 정렬 (연도 순서대로)
df['시작연도'] = df['제설시즌'].str[:4].astype(int)
df = df.sort_values(by='시작연도')

# 꺾은선 그래프 그리기
plt.figure(figsize=(10, 6))
plt.plot(df['제설시즌'], df['합계'], marker='o', label='포트홀 발생 합계')
plt.plot(df['제설시즌'], df['사용량(톤)'], marker='s', label='제설제 사용량 (톤)')

plt.xlabel('제설 시즌 (년도)')
plt.ylabel('값')
plt.title('제설 시즌별 포트홀 발생 합계 및 제설제 사용량 추이')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
