import pandas as pd

# 파일 경로
file_path = r"C:\Users\GME-NOTE\Desktop\EDB_PJT\ORG_DATA\1_서울시 포트홀 보수 위치 정보\서울시 포트홀 보수 위치 정보.xlsx"

# 엑셀 데이터 전체 불러오기 (첫 시트 기준)
df = pd.read_excel(file_path)

# '등록번호'에서 2023으로 시작하는 데이터만 필터링
df_2023 = df[df['등록번호'].astype(str).str.startswith('2023')].copy()

# 결과 확인
print(df_2023.head())

# 저장 (선택)
save_path = r"/ANALYSIS_DATA/교통량/포트홀_2023년_데이터만.csv"
df_2023.to_csv(save_path, index=False, encoding='utf-8-sig')
