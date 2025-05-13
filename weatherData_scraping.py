import requests
import xml.etree.ElementTree as ET

# 워드 파일 기반 한글 설명 매핑
field_mapping = {
    "stnId": "지점 번호",
    "stnNm": "지점명",
    "tm": "날짜",
    "avgTa": "평균 기온(°C)",
    "minTa": "최저 기온(°C)",
    "minTaHrmt": "최저 기온 시각(hhmm)",
    "maxTa": "최고 기온(°C)",
    "maxTaHrmt": "최고 기온 시각(hhmm)",
    "mi10MaxRn": "10분 최다강수량(mm)",
    "mi10MaxRnHrmt": "10분 최다강수 시각(hhmm)",
    "hr1MaxRn": "1시간 최다강수(mm)",
    "hr1MaxRnHrmt": "1시간 최다강수 시각(hhmm)",
    "sumRnDur": "강수 계속시간(hr)",
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
    "minRhmHrmt": "최소 상대습도 시각(hhmm)",
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

# API 호출
url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
params = {
    'serviceKey': 'FRBg0qFrrlGH290TSHXY/TnRZnRmiIpIkVoYbNcd98zd3+YCpYKOlgJbrTee+VDIpeCTyPncmPo0g0b1SZAZMg==',
    'pageNo': '1',
    'numOfRows': '100',
    'dataType': 'XML',
    'dataCd': 'ASOS',
    'dateCd': 'DAY',
    'startDt': '20100101',
    'endDt': '20100601',
    'stnIds': '108'
}

response = requests.get(url, params=params)
root = ET.fromstring(response.content)

items = root.find('body').find('items')
print(f"총 {len(items)}개의 데이터가 수신되었습니다.\n")

# 데이터 출력
for idx, item in enumerate(items.findall('item'), start=1):
    날짜 = item.findtext('tm', 'N/A')
    지점명 = item.findtext('stnNm', 'N/A')
    지점번호 = item.findtext('stnId', 'N/A')
    print(f"[{idx}] 날짜: {날짜} | 지점명: {지점명} ({지점번호})")
    print("-" * 60)

    for child in item:
        tag = child.tag
        val = child.text.strip() if child.text else 'N/A'
        label = field_mapping.get(tag, tag)  # 한글 매핑 없으면 그대로 출력
        print(f"{label:<25}: {val}")

    print("=" * 60)
