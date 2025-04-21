
from firebase_service import get_data_from_firebase
from database import connect_mysql, get_input_data_from_mysql
from forecast import forecast_24h , forecast_7d
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.losses import MeanSquaredError
import time

if __name__ == "__main__":
    print("⏳ Đang tải mô hình...")
    custom_objects = {'mse': MeanSquaredError()}
    model_24h = tf.function(load_model("D:\\SERVER_DBTT\\dubao.keras", custom_objects=custom_objects))
    model_7d = tf.function(load_model("D:\\SERVER_DBTT\\dubao_7d.keras", custom_objects=custom_objects))
    print("✅ Mô hình đã sẵn sàng!")

    while True:
        try:
            # get_data_from_firebase()  # Nếu cần
            forecast_24h(model_24h)
            forecast_7d(model_7d)
            print("🕐 Đang chờ dự báo tiếp theo ...\n")
            time.sleep(60)
        except Exception as e:
            print(f"❌ Lỗi trong vòng lặp: {e}")
            time.sleep(60)

