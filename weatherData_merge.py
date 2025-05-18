import pandas as pd

# 파일 경로
file_path = r"C:\Users\GME-NOTE\Desktop\EDB_PJT\ORG_DATA\6_날씨 데이터\서울_날씨_2013_2024_통합_일별.csv"

# CSV 읽기
df = pd.read_csv(file_path, encoding='utf-8-sig')

# 날짜 컬럼 변환
df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
df['연월'] = df['날짜'].dt.to_period('M')

# 수치형 컬럼만 선택
numeric_df = df.select_dtypes(include=['number'])

# '연월'과 수치형 컬럼 병합
numeric_df['연월'] = df['연월']

# 월별 평균 계산
monthly_avg = numeric_df.groupby('연월').mean().round(1).reset_index()

# 결과 출력
print(monthly_avg.head())

# 결과 저장
output_path = file_path.replace('.csv', '_월별평균_전체지표.csv')
monthly_avg.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"\n✅ 월별 평균 저장 완료 (소수점 1자리): {output_path}")
