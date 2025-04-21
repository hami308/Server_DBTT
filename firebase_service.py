import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
from firebase_config import FIREBASE_URL, FIREBASE_KEY_PATH
from database import save_firebase_data_to_mysql    


# # Kiểm tra và khởi tạo Firebase nếu chưa có
# if not firebase_admin._apps:
#     cred = credentials.Certificate(FIREBASE_KEY_PATH)
#     firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_URL})


# Hàm lấy dữ liệu từ Firebase
def get_data_from_firebase():
    ref = db.reference("/weather_data")  # Node chứa dữ liệu
    data = ref.get()

    if not data:
        print("❌ Không có dữ liệu từ Firebase.")
        return

    try:
        # Lấy thời gian hiện tại
        now = datetime.now()
        year, month, day, hour = now.year, now.month, now.day, now.hour

        # Trích xuất dữ liệu từ Firebase
        humidity = data.get("humidity", 0.0)  # QV2M
        rain = data.get("rain", 0.0)  # PRECTOTCORR
        pressure = data.get("pressure", 0.0)  # PS
        temperature = data.get("temperature", 0.0)  # T2M
        light = data.get("light", 0.0)  # ALLSKY_SFC_PAR_TOT

            # Gửi dữ liệu đến MySQL
        save_firebase_data_to_mysql (year, month, day, hour, humidity, rain, pressure, temperature, light)

    except Exception as e:
        print(f"⚠️ Lỗi khi xử lý dữ liệu: {e}")

# Hàm đẩy dữ liệu dự báo lên Firebase
def push_forecast_to_firebase(du_bao_24h_df):
    ref = db.reference("/weather_24h")
    du_bao_dict = du_bao_24h_df.to_dict(orient='index')

    # Định dạng dữ liệu để lưu lên Firebase
    formatted_data = {str(k): v for k, v in du_bao_dict.items()}
    ref.set(formatted_data)

    print("✅ Dữ liệu 24h đã được đẩy lên Firebase thành công!")
def push_forecast_7d_to_firebase(du_bao_7d_df):
    ref = db.reference("/weather_7d")
    du_bao_dict = du_bao_7d_df.to_dict(orient='index')

    # Định dạng dữ liệu để lưu lên Firebase
    formatted_data = {str(k): v for k, v in du_bao_dict.items()}
    ref.set(formatted_data)

    print("✅ Dữ liệu 7d đã được đẩy lên Firebase thành công!")
