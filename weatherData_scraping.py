import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os
from datetime import datetime, timedelta

# 저장 경로
save_dir = r"C:\Users\GME-NOTE\Desktop\EDB_PJT\ORG_DATA\6_날씨 데이터"
os.makedirs(save_dir, exist_ok=True)

# 날짜 설정
start_date = datetime.strptime('20130101', "%Y%m%d")
end_date = datetime.strptime('20131231', "%Y%m%d")

# 지점 ID 및 이름
station_id = '108'  # 서울
station_name = '서울'

# 데이터 필드 매핑
field_mapping = {
    "stnId": "지점 번호",
    "stnNm": "지점명",
    "tm": "날짜",
    "avgTa": "평균 기온(°C)",
    "minTa": "최저 기온(°C)",
    "minTaHrmt": "최저 기온 시각(hhmm)",
    "maxTa": "최고 기온(°C)",
    "maxTaHrmt": "최고 기온 시각(hhmm)",
    "sumRnDur": "강수 계속시간(hr)",
    "mi10MaxRn": "10분 최다강수량(mm)",
    "mi10MaxRnHrmt": "10분 최다강수 시각(hhmm)",
    "hr1MaxRn": "1시간 최다강수(mm)",
    "hr1MaxRnHrmt": "1시간 최다강수 시각(hhmm)",
    "sumRn": "일강수량(mm)",
    "maxInsWs": "최대 순간풍속(m/s)",
    "maxInsWsWd": "최대 순간 풍속 풍향(16방위)",
    "maxInsWsHrmt": "최대 순간풍속 시각(hhmm)",
    "maxWs": "최대 풍속(m/s)",
    "maxWsWd": "최대 풍속 풍향(16방위)",
    "maxWsHrmt": "최대 풍속 시각(hhmm)",
    "avgWs": "평균 풍속(m/s)",
    "hr24SumRws": "풍정합(100m)",
    "maxWd": "최다 풍향(16방위)",
    "avgTd": "평균 이슬점온도(°C)",
    "minRhm": "최소 상대습도(%)",
    "minRhmHrmt": "평균 상대습도 시각(hhmm)",
    "avgRhm": "평균 상대습도(%)",
    "avgPv": "평균 증기압(hPa)",
    "avgPa": "평균 현지기압(hPa)",
    "maxPs": "최고 해면기압(hPa)",
    "maxPsHrmt": "최고 해면기압 시각(hhmm)",
    "minPs": "최저 해면기압(hPa)",
    "minPsHrmt": "최저 해면기압 시각(hhmm)",
    "avgPs": "평균 해면기압(hPa)",
    "ssDur": "가조시간(hr)",
    "sumSsHr": "합계 일조 시간(hr)",
    "hr1MaxIcsrHrmt": "1시간 최다 일사 시각(hhmm)",
    "hr1MaxIcsr": "1시간 최다 일사량(MJ/m2)",
    "sumGsr": "합계 일사량(MJ/m2)",
    "ddMefs": "일 최심신적설(cm)",
    "ddMefsHrmt": "일 최심신적설 시각(hhmm)",
    "ddMes": "일 최심적설(cm)",
    "ddMesHrmt": "일 최심적설 시각(hhmm)",
    "sumDpthFhsc": "합계 3시간 신적설(cm)",
    "avgTca": "평균 전운량(10분위)",
    "avgLmac": "평균 중하층운량(10분위)",
    "avgTs": "평균 지면온도(°C)",
    "minTg": "최저 초상온도(°C)",
    "avgCm5Te": "5cm 지중온도(°C)",
    "avgCm10Te": "10cm 지중온도(°C)",
    "avgCm20Te": "20cm 지중온도(°C)",
    "avgCm30Te": "30cm 지중온도(°C)",
    "avgM05Te": "0.5m 지중온도(°C)",
    "avgM10Te": "1.0m 지중온도(°C)",
    "avgM15Te": "1.5m 지중온도(°C)",
    "avgM30Te": "3.0m 지중온도(°C)",
    "avgM50Te": "5.0m 지중온도(°C)",
    "sumLrgEv": "합계 대형증발량(mm)",
    "sumSmlEv": "합계 소형증발량(mm)",
    "n99Rn": "9-9강수(mm)",
    "iscs": "일기현상",
    "sumFogDur": "안개 계속 시간(hr)"
}


# API 요청 기본 정보
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
service_key = 'FRBg0qFrrlGH290TSHXY/TnRZnRmiIpIkVoYbNcd98zd3+YCpYKOlgJbrTee+VDIpeCTyPncmPo0g0b1SZAZMg=='

current_date = start_date
data_by_year = {}

print(f"⏳ 수집 시작: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")

while current_date <= end_date:
    dt_str = current_date.strftime("%Y%m%d")
    year = current_date.year

    params = {
        'serviceKey': service_key,
        'pageNo': '1',
        'numOfRows': '100',
        'dataType': 'XML',
        'dataCd': 'ASOS',
        'dateCd': 'DAY',
        'startDt': dt_str,
        'endDt': dt_str,
        'stnIds': station_id
    }

    # 최대 3회 재시도
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, params=params, timeout=10)
            root = ET.fromstring(response.content)

            body = root.find('body')
            if body is None:
                raise ValueError("응답에 <body> 없음")

            items = body.find('items')
            if items is None:
                print(f"[{dt_str}] 데이터 없음.")
                break  # 데이터 없는 건 재시도 안 함

            for item in items.findall('item'):
                row = {}
                for child in item:
                    tag = child.tag
                    val = child.text.strip() if child.text else 'N/A'
                    label = field_mapping.get(tag, tag)
                    row[label] = val
                data_by_year.setdefault(year, []).append(row)

            if current_date.day == 1:
                print(f"\n📆 {year}년 {current_date.strftime('%m월')} 처리 중...")

            break  # 성공하면 재시도 탈출

        except Exception as e:
            print(f"⚠️ 오류 발생: {dt_str} | {e} (시도 {attempt}/{max_retries})")
            if attempt == max_retries:
                print(f"❌ {dt_str} 최종 실패. 스킵됨.\n")

    # 다음 날짜로 이동
    next_day = current_date + timedelta(days=1)

    # 연도 경계 도달 시 저장 및 무결성 검사
    if (year != next_day.year) or (next_day > end_date):
        if year in data_by_year:
            df_year = pd.DataFrame(data_by_year[year])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{station_name}_날씨_{year}_{timestamp}.csv"
            filepath = os.path.join(save_dir, filename)
            df_year.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"✅ 저장 완료: {filename} ({len(df_year)}건)")

            # ✅ 무결성 검사
            try:
                df_check = pd.read_csv(filepath, encoding='utf-8-sig')
                df_check['날짜'] = pd.to_datetime(df_check['날짜'], errors='coerce')

                year_start = datetime(year, 1, 1)
                year_end = datetime(year, 12, 31)
                if year == end_date.year:
                    year_end = end_date

                expected = set(pd.date_range(year_start, year_end))
                actual = set(df_check['날짜'].dropna())

                missing = sorted(expected - actual)
                if missing:
                    print(f"⚠️ 무결성 오류: {year}년 누락된 날짜 {len(missing)}일")
                    for d in missing[:5]:
                        print(f"   - {d.strftime('%Y-%m-%d')}")
                    if len(missing) > 5:
                        print(f"   ... (이하 {len(missing)-5}개 생략)")
                else:
                    print(f"🟢 무결성 검사 통과: {year}년 모든 날짜 포함됨")
            except Exception as e:
                print(f"❌ 무결성 검사 실패: {e}")

            del data_by_year[year]

    current_date += timedelta(days=1)

print("\n🎉 전체 저장 및 무결성 검사 완료!")