import requests
import json
import pandas as pd
from datetime import datetime
import time
import os

# 경로 설정
save_dir = r"C:/Users/GME-NOTE/Desktop/EDB_PJT/NAVIGATION/포트홀감지"
log_path = os.path.join(save_dir, "log.txt")

# API 기본 정보
api_key = "ff53611e-25ab-485e-9eb2-c3bec426f6a7"
base_url = "http://t-data.seoul.go.kr/apig/apiman-gateway/tapi/v2xPotholeInformation/1.0"

# 무한 반복
while True:
    try:
        # 요청 파라미터
        params = {
            'apikey': api_key,
            'type': 'json',
            'pageNo': 1,
            'numOfRows': 2
        }

        # API 요청
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()

            for item in data:
                lat = item.get("vhcleLat")
                lon = item.get("vhcleLot")
                dows = item.get("dowsCd")
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # 로그 메시지 구성
                log_message = f"[{now_str}] 위도: {lat}, 경도: {lon}, dowsCd: {dows}"
                print(log_message)

                # 로그 파일에 추가 기록
                with open(log_path, "a", encoding="utf-8") as log_file:
                    log_file.write(log_message + "\n")

                # dowsCd가 1일 경우만 CSV 저장
                if dows == "1":
                    df = pd.DataFrame([[lat, lon, dows]], columns=["latitude", "longitude", "dowsCd"])
                    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
                    filename = f"포트홀_위치_요약_{timestamp}.csv"
                    full_path = os.path.join(save_dir, filename)
                    df.to_csv(full_path, index=False, encoding="utf-8-sig")
                    print(f"📁 저장 완료: {filename}")

        else:
            print(f"❌ 요청 실패: 상태 코드 {response.status_code}")

    except Exception as e:
        error_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_message = f"[{error_time}] ⚠️ 오류 발생: {e}"
        print(error_message)
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(error_message + "\n")

    # 호출 간 간격 설정 (초)
    time.sleep(10)
