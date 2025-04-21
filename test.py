import requests
import pandas as pd
from datetime import datetime, timedelta

# API Key và địa điểm
api_key = 'GWZMUWHZUHCA7RWZEXCMMKFLY'
location = 'Da Nang'

# Lấy thời gian hiện tại và lùi về 12 giờ trước
end_time = datetime.now()
start_time = end_time - timedelta(hours=12)

# Định dạng thời gian (Visual Crossing chỉ chấp nhận định dạng YYYY-MM-DDTHH:mm:ss)
start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')
end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S')

# Gọi API lấy dữ liệu theo giờ
url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}/{start_str}/{end_str}?unitGroup=metric&key={api_key}&include=hours&contentType=csv'

response = requests.get(url)

# Lưu dữ liệu CSV
with open('weather_danang_last_12h.csv', 'wb') as f:
    f.write(response.content)

# Đọc dữ liệu và hiển thị cột mong muốn
df = pd.read_csv('weather_danang_last_12h.csv')

# In ra thông tin 12 giờ gần nhất
print(df[['datetime', 'temp', 'humidity', 'precip', 'precipprob', 'pressure', 'solarenergy']])


# import pandas as pd
# import mysql.connector
# from datetime import datetime

# # Hàm kết nối đến MySQL
# def connect_mysql():
#     return mysql.connector.connect(
#         host="localhost",        # Đổi nếu MySQL không chạy local
#         user="root",        # Tên người dùng MySQL
#         password="",# Mật khẩu
#         database="dubaothoitiet" # Tên CSDL
#     )

# # Hàm lưu dữ liệu vào bảng weather_data
# def save_firebase_data_to_mysql(year, month, day, hour, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT):
#     try:
#         conn = connect_mysql()
#         cursor = conn.cursor()

#         sql = """
#             INSERT INTO weather_data 
#             (YEAR, MO, DY, HR, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT) 
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#             ON DUPLICATE KEY UPDATE 
#                 QV2M = VALUES(QV2M), 
#                 PRECTOTCORR = VALUES(PRECTOTCORR), 
#                 PS = VALUES(PS), 
#                 T2M = VALUES(T2M), 
#                 ALLSKY_SFC_PAR_TOT = VALUES(ALLSKY_SFC_PAR_TOT)
#         """
#         values = (year, month, day, hour, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT)

#         cursor.execute(sql, values)
#         conn.commit()
#         cursor.close()
#         conn.close()

#     except Exception as e:
#         print(f"⚠️ Lỗi khi lưu dữ liệu vào MySQL: {e}")

# # Đọc file Excel (hoặc CSV)
# df = pd.read_csv('weather_danang_hourly.csv')

# # Tách datetime thành YEAR, MO, DY, HR
# dt = pd.to_datetime(df['datetime'])
# df['YEAR'] = dt.dt.year
# df['MO'] = dt.dt.month
# df['DY'] = dt.dt.day
# df['HR'] = dt.dt.hour

# # Lọc các cột cần thiết
# df_filtered = df[['YEAR', 'MO', 'DY', 'HR', 'QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']]

# # Lưu từng dòng vào MySQL
# for index, row in df_filtered.iterrows():
#     save_firebase_data_to_mysql(
#         year=int(row['YEAR']),
#         month=int(row['MO']),
#         day=int(row['DY']),
#         hour=int(row['HR']),
#         QV2M=float(row['QV2M']),
#         PRECTOTCORR=float(row['PRECTOTCORR']),
#         PS=float(row['PS']),
#         T2M=float(row['T2M']),
#         ALLSKY_SFC_PAR_TOT=float(row['ALLSKY_SFC_PAR_TOT'])
#     )

# print("✅ Hoàn tất lưu dữ liệu vào MySQL.")

