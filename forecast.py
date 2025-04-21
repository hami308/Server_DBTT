import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.losses import MeanSquaredError
from database import get_input_data_from_mysql  # Lấy dữ liệu từ MySQL
from firebase_service import push_forecast_to_firebase , push_forecast_7d_to_firebase  # Đẩy dữ liệu lên Firebase
# def forecast_24h():
#     # 1. Lấy dữ liệu từ MySQL
#     df = get_input_data_from_mysql()
#     if df is None or len(df) < 24:
#         print("⚠ Không đủ dữ liệu đầu vào để dự báo!")
#         return

#     # 2. Chọn cột cần thiết cho dự báo
#     thong_so = ['QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']
#     df = df[thong_so]

#     # 3. Tiền xử lý dữ liệu
#     scaler = StandardScaler()
#     du_lieu_chuan_hoa = scaler.fit_transform(df)

#     # 4. Chuẩn bị dữ liệu đầu vào cho mô hình (luôn lấy 24 giờ cuối)
#     buoc_nhap = 24
#     if len(du_lieu_chuan_hoa) >= buoc_nhap:
#         X = np.array([du_lieu_chuan_hoa[-buoc_nhap:]])  # Giữ nguyên kích thước cố định (1, 24, số lượng đặc trưng)
#     else:
#         print("⚠ Không đủ dữ liệu để tạo đầu vào!")
#         return

#     # 5. Tải mô hình dự báo
#     custom_objects = {'mse': MeanSquaredError()}
#     model = load_model("D:\\SERVER_DBTT\\dubao.keras", custom_objects=custom_objects)

#     # 6. Dự báo 24 giờ tiếp theo (Dùng tf.function để giảm retracing)
#     @tf.function(reduce_retracing=True)
#     def du_doan(model, X):
#         return model(X)

#     Y_du_doan = du_doan(model, X).numpy()  # Chuyển kết quả về numpy

#     # 7. Biến đổi dữ liệu về giá trị gốc
#     Y_du_doan_reshaped = Y_du_doan.reshape(-1, X.shape[2])
#     Y_du_doan_nguyen = scaler.inverse_transform(Y_du_doan_reshaped)
#     Y_du_doan_nguyen = Y_du_doan_nguyen.reshape(Y_du_doan.shape)

#     # 8. Lấy dự báo 24 giờ tiếp theo
#     du_bao_24h = Y_du_doan_nguyen[0]  # Lấy kết quả dự báo duy nhất

#     # 9. Tạo DataFrame kết quả dự báo
#     du_bao_24h_df = pd.DataFrame(du_bao_24h, columns=thong_so)
#     du_bao_24h_df['PRECTOTCORR'] = du_bao_24h_df['PRECTOTCORR'].clip(lower=0)
#     du_bao_24h_df['ALLSKY_SFC_PAR_TOT'] = du_bao_24h_df['ALLSKY_SFC_PAR_TOT'].clip(lower=0)


#     # 10. Xác định khoảng thời gian cho dự báo
#     last_time = df.index[-1]
#     thoi_gian_du_bao = pd.date_range(start=last_time + pd.Timedelta(hours=1), periods=24, freq='h')
#     du_bao_24h_df.index = thoi_gian_du_bao
#     du_bao_24h_df.index.name = 'thoigian'

#     # 11. In kết quả dự báo
#     print("✅ Dự báo 24 giờ tiếp theo:")
#     print(du_bao_24h_df)

#     # 12. Đẩy kết quả lên Firebase
#     push_forecast_to_firebase(du_bao_24h_df)

# def forecast_7d():
#     # 1. Lấy dữ liệu từ MySQL
#     df = get_input_data_from_mysql(so_gio=168)  # Lấy 7 ngày (168 giờ)
#     if df is None or len(df) < 168:
#         print("⚠ Không đủ dữ liệu đầu vào để dự báo!")
#         return

#     # 2. Chọn cột cần thiết cho dự báo
#     thong_so = ['QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']
#     df = df[thong_so]

#     # 3. Tiền xử lý dữ liệu
#     scaler = StandardScaler()
#     du_lieu_chuan_hoa = scaler.fit_transform(df)

#     # 4. Chuẩn bị dữ liệu đầu vào cho mô hình (luôn lấy 24 giờ cuối)
#     buoc_nhap = 168
#     if len(du_lieu_chuan_hoa) >= buoc_nhap:
#         X = np.array([du_lieu_chuan_hoa[-buoc_nhap:]])  # Giữ nguyên kích thước cố định (1, 24, số lượng đặc trưng)
#     else:
#         print("⚠ Không đủ dữ liệu để tạo đầu vào!")
#         return

#     # 5. Tải mô hình dự báo
#     custom_objects = {'mse': MeanSquaredError()}
#     model = load_model("D:\\SERVER_DBTT\\dubao_7d.keras", custom_objects=custom_objects)

#     # 6. Dự báo 7day tiếp theo (Dùng tf.function để giảm retracing)
#     @tf.function(reduce_retracing=True)
#     def du_doan(model, X):
#         return model(X)

#     Y_du_doan = du_doan(model, X).numpy()  # Chuyển kết quả về numpy

#     # 7. Biến đổi dữ liệu về giá trị gốc
#     Y_du_doan_reshaped = Y_du_doan.reshape(-1, X.shape[2])
#     Y_du_doan_nguyen = scaler.inverse_transform(Y_du_doan_reshaped)
#     Y_du_doan_nguyen = Y_du_doan_nguyen.reshape(Y_du_doan.shape)

#     # 8. Lấy dự báo 24 giờ tiếp theo
#     du_bao_7d = Y_du_doan_nguyen[0]  # Lấy kết quả dự báo duy nhất

#     # 9. Tạo DataFrame kết quả dự báo
#     du_bao_7d_df = pd.DataFrame(du_bao_7d, columns=thong_so)
#     du_bao_7d_df['PRECTOTCORR'] = du_bao_7d_df['PRECTOTCORR'].clip(lower=0)
#     du_bao_7d_df['ALLSKY_SFC_PAR_TOT'] = du_bao_7d_df['ALLSKY_SFC_PAR_TOT'].clip(lower=0)


#     # 10. Xác định khoảng thời gian cho dự báo
#     last_time = df.index[-1]
#     thoi_gian_du_bao = pd.date_range(start=last_time + pd.Timedelta(hours=1), periods=168, freq='h')
#     du_bao_7d_df.index = thoi_gian_du_bao
#     du_bao_7d_df.index.name = 'thoigian'

#     # 12. Tính min/max mỗi ngày cho các thông số chính
#     du_bao_ngay = du_bao_7d_df.resample('D').agg({
#         'T2M': ['min', 'max'],
#         'QV2M': ['min', 'max'],
#         'PRECTOTCORR': ['min', 'max']
#     })
#     # Đổi tên 
#     du_bao_ngay.columns = ['T2M_min', 'T2M_max', 'QV2M_min', 'QV2M_max', 'PRECTOTCORR_min', 'PRECTOTCORR_max']

#     # In ra bảng tổng hợp
#     print("\n📊 Thống kê dự báo từng ngày:")
#     print(du_bao_ngay)
    
#     du_bao_ngay.index = du_bao_ngay.index.strftime('%Y-%m-%d')  # Bỏ giờ
#     push_forecast_to_firebase(du_bao_ngay)  # Đẩy lên Firebase
#     # # 11. In kết quả dự báo
#     # print("✅ Dự báo 168 giờ tiếp theo:")
#     # print(du_bao_7d_df)

# ____________________________________________________________________________________
# Dự báo 24h
def forecast_24h(model_24h):
    df = get_input_data_from_mysql()
    if df is None or len(df) < 24:
        print("⚠ Không đủ dữ liệu đầu vào để dự báo 24h!")
        return

    thong_so = ['QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']
    df = df[thong_so]

    scaler = StandardScaler()
    du_lieu_chuan_hoa = scaler.fit_transform(df)
    
    buoc_nhap = 24
    X = np.array([du_lieu_chuan_hoa[-buoc_nhap:]])

    Y_du_doan = model_24h(X).numpy()
    Y_du_doan_nguyen = scaler.inverse_transform(Y_du_doan.reshape(-1, X.shape[2])).reshape(Y_du_doan.shape)
    
    du_bao_24h_df = pd.DataFrame(Y_du_doan_nguyen[0], columns=thong_so)
    du_bao_24h_df['PRECTOTCORR'] = du_bao_24h_df['PRECTOTCORR'].clip(lower=0)
    du_bao_24h_df['ALLSKY_SFC_PAR_TOT'] = du_bao_24h_df['ALLSKY_SFC_PAR_TOT'].clip(lower=0)

    last_time = df.index[-1]
    du_bao_24h_df.index = pd.date_range(start=last_time + pd.Timedelta(hours=1), periods=24, freq='h')
    du_bao_24h_df.index.name = 'thoigian'

    print("✅ Dự báo 24 giờ tiếp theo:")
    print(du_bao_24h_df)
    push_forecast_to_firebase(du_bao_24h_df)

# Dự báo 7 ngày
def forecast_7d(model_7d):
    df = get_input_data_from_mysql(so_gio=168)
    if df is None or len(df) < 168:
        print("⚠ Không đủ dữ liệu đầu vào để dự báo 7 ngày!")
        return

    thong_so = ['QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']
    df = df[thong_so]

    scaler = StandardScaler()
    du_lieu_chuan_hoa = scaler.fit_transform(df)

    buoc_nhap = 168
    X = np.array([du_lieu_chuan_hoa[-buoc_nhap:]])

    Y_du_doan = model_7d(X).numpy()
    Y_du_doan_nguyen = scaler.inverse_transform(Y_du_doan.reshape(-1, X.shape[2])).reshape(Y_du_doan.shape)

    du_bao_7d_df = pd.DataFrame(Y_du_doan_nguyen[0], columns=thong_so)
    du_bao_7d_df['PRECTOTCORR'] = du_bao_7d_df['PRECTOTCORR'].clip(lower=0)
    du_bao_7d_df['ALLSKY_SFC_PAR_TOT'] = du_bao_7d_df['ALLSKY_SFC_PAR_TOT'].clip(lower=0)

    last_time = df.index[-1]
    du_bao_7d_df.index = pd.date_range(start=last_time + pd.Timedelta(hours=1), periods=168, freq='h')
    du_bao_7d_df.index.name = 'thoigian'

    du_bao_ngay = du_bao_7d_df.resample('D').agg({
        'T2M': ['min', 'max'],
        'QV2M': 'mean',
        'PRECTOTCORR': 'mean',
        'PS': 'mean',
        'ALLSKY_SFC_PAR_TOT': 'mean'
    })
    du_bao_ngay.columns = ['T2M_min', 'T2M_max', 'QV2M', 'PRECTOTCORR', 'PS', 'ALLSKY_SFC_PAR_TOT']
    du_bao_ngay.index = du_bao_ngay.index.strftime('%Y-%m-%d')

    print("\n📊 Thống kê dự báo từng ngày:")
    print(du_bao_ngay)
    push_forecast_7d_to_firebase(du_bao_ngay)  # Đẩy lên
