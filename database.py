import mysql.connector
import numpy as np
import pandas as pd
MYSQL_CONFIG = {    # Thông tin kết nối MySQL   
    "host": "localhost",
    "user":"root",
    "password":"",
    "database":"dubaothoitiet",
}

def connect_mysql():
    return mysql.connector.connect(**MYSQL_CONFIG)
db = connect_mysql()
cursor = db.cursor()
def save_firebase_data_to_mysql(year, month, day, hour, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT):
    try:
        conn = connect_mysql()
        cursor = conn.cursor()

        sql = """INSERT INTO weather_data (YEAR, MO, DY, HR, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                 ON DUPLICATE KEY UPDATE 
                 QV2M = VALUES(QV2M), 
                 PRECTOTCORR = VALUES(PRECTOTCORR), 
                 PS = VALUES(PS), 
                 T2M = VALUES(T2M), 
                 ALLSKY_SFC_PAR_TOT = VALUES(ALLSKY_SFC_PAR_TOT)"""
        values = (year, month, day, hour, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT)

        cursor.execute(sql, values)
        conn.commit()
        print("✅ Dữ liệu đã được lưu vào MySQL.")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"⚠️ Lỗi khi lưu dữ liệu vào MySQL: {e}")
def get_input_data_from_mysql(so_gio=24):
    query = f"""
        SELECT * 
        FROM (
            SELECT YEAR, MO, DY, HR, QV2M, PRECTOTCORR, PS, T2M, ALLSKY_SFC_PAR_TOT
            FROM weather_data
            ORDER BY YEAR DESC, MO DESC, DY DESC, HR DESC
            LIMIT {so_gio}
        ) AS subquery
        ORDER BY YEAR ASC, MO ASC, DY ASC, HR ASC;
    """

    conn = connect_mysql()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        print("❌ Không có dữ liệu thời tiết trong MySQL!")
        return None

    # Tạo DataFrame
    df = pd.DataFrame(rows, columns=['YEAR', 'MO', 'DY', 'HR', 'QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT'])

    # Tạo datetime index
    df['datetime'] = pd.to_datetime(df[['YEAR', 'MO', 'DY', 'HR']].rename(columns={
        'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'
    }))
    df.set_index('datetime', inplace=True)

    # Chỉ giữ các cột cần thiết
    thong_so = ['QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']
    df = df[thong_so]

    # print(f"✅ Dữ liệu đầu vào của mô hình ({so_gio} giờ):")
    # print(df)

    return df
