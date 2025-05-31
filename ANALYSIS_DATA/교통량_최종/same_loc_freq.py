import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

# 한글 폰트 설정 (Windows 기준)
matplotlib.rcParams['font.family'] = 'Malgun Gothic'
matplotlib.rcParams['axes.unicode_minus'] = False

# 1. 엑셀 데이터 불러오기
file_path = r"도로별_포트홀 빈도수 분석용.xlsx"
df = pd.read_excel(file_path)

# 2. 도로명주소별 포트홀 발생 횟수 계산
frequency = df["도로명주소"].value_counts().reset_index()
frequency.columns = ["도로명주소", "포트홀_발생횟수"]

# 3. 상위 20개 도로 추출
top20 = frequency.head(20)

# 4. 그래프 생성 및 저장
plt.figure(figsize=(12, 8))
plt.barh(top20["도로명주소"], top20["포트홀_발생횟수"], color='coral')
plt.xlabel("포트홀 발생 횟수")
plt.title("같은 위치에서 반복된 포트홀 발생 상위 20개 도로")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(r"05_포트홀_반복발생_상위20.png")
plt.close()
