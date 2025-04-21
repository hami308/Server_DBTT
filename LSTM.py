import pandas as pd

df = pd.read_csv('datathoitiet.csv', skiprows=13)
print(df.head())

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
#from tensorflow.python.keras.models import Sequential
#from tensorflow.python.keras.layers import  Dense, LSTM, TimeDistributed, Input
#import tensorflow as tf

from tensorflow.keras.models import Sequential  # Sử dụng đường dẫn chuẩn
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed, Input  # Sử dụng đường dẫn chuẩn
import tensorflow as tf

import matplotlib.pyplot as plt

df = pd.read_csv('datathoitiet.csv', skiprows=13)

df.columns = df.columns.str.strip()

print("Tên các cột:", df.columns)
print("Dữ liệu đầu tiên:\n", df.head())

df['thoigian'] = pd.to_datetime(df[['YEAR', 'MO', 'DY', 'HR']].rename(
    columns={'YEAR': 'year', 'MO': 'month', 'DY': 'day', 'HR': 'hour'}
))

df.set_index('thoigian', inplace=True)
df.drop(['YEAR', 'MO', 'DY', 'HR'], axis=1, inplace=True)

df.replace(-999, np.nan, inplace=True)
df.interpolate(method='linear', inplace=True)

ngay_ket_thuc_huan_luyen = '2024-03-04 23:00:00'
tap_huan_luyen = df.loc[:ngay_ket_thuc_huan_luyen]
tap_kiem_tra = df.loc[ngay_ket_thuc_huan_luyen:]

scaler = StandardScaler()
du_lieu_huan_luyen_chuan_hoa = scaler.fit_transform(tap_huan_luyen)
du_lieu_kiem_tra_chuan_hoa = scaler.transform(tap_kiem_tra)

tap_huan_luyen_chuan_hoa = pd.DataFrame(du_lieu_huan_luyen_chuan_hoa,
                                        columns=tap_huan_luyen.columns,
                                        index=tap_huan_luyen.index)
tap_kiem_tra_chuan_hoa = pd.DataFrame(du_lieu_kiem_tra_chuan_hoa,
                                      columns=tap_kiem_tra.columns,
                                      index=tap_kiem_tra.index)

def tao_chuoi_du_lieu(du_lieu, buoc_nhap, buoc_xuat):
    X, Y = [], []
    for i in range(len(du_lieu) - buoc_nhap - buoc_xuat + 1):
        X.append(du_lieu[i:i + buoc_nhap])
        Y.append(du_lieu[i + buoc_nhap:i + buoc_nhap + buoc_xuat])
    return np.array(X), np.array(Y)

buoc_nhap = 168
buoc_xuat = 168

du_lieu_huan_luyen = tap_huan_luyen_chuan_hoa.values
du_lieu_kiem_tra = tap_kiem_tra_chuan_hoa.values

X_huan_luyen, Y_huan_luyen = tao_chuoi_du_lieu(du_lieu_huan_luyen, buoc_nhap, buoc_xuat)
X_kiem_tra, Y_kiem_tra = tao_chuoi_du_lieu(du_lieu_kiem_tra, buoc_nhap, buoc_xuat)

model = Sequential()
model.add(Input(shape=(buoc_nhap, X_huan_luyen.shape[2])))  # 👈 Thêm lớp Input
model.add(LSTM(64, return_sequences=True))
model.add(TimeDistributed(Dense(X_huan_luyen.shape[2])))
model.compile(loss='mse', optimizer='adam')

model.fit(X_huan_luyen, Y_huan_luyen, epochs=20, batch_size=32, validation_split=0.2, verbose=1)
model.save('D:\\SERVER_DBTT\\dubao_7d7d.keras')
Y_du_doan = model.predict(X_kiem_tra)

Y_du_doan_reshaped = Y_du_doan.reshape(-1, X_kiem_tra.shape[2])
Y_du_doan_nguyen = scaler.inverse_transform(Y_du_doan_reshaped)
Y_du_doan_nguyen = Y_du_doan_nguyen.reshape(Y_du_doan.shape)

Y_kiem_tra_reshaped = Y_kiem_tra.reshape(-1, X_kiem_tra.shape[2])
Y_kiem_tra_nguyen = scaler.inverse_transform(Y_kiem_tra_reshaped)
Y_kiem_tra_nguyen = Y_kiem_tra_nguyen.reshape(Y_kiem_tra.shape)

thong_so = ['QV2M', 'PRECTOTCORR', 'PS', 'T2M', 'ALLSKY_SFC_PAR_TOT']

for i, param in enumerate(thong_so):
    mae = mean_absolute_error(Y_kiem_tra_nguyen[:, :, i].flatten(), Y_du_doan_nguyen[:, :, i].flatten())
    print(f"MAE cho {param}: {mae}")

tieu_de = {
    'QV2M': 'Độ Ẩm Tỷ Đối (g/kg)',
    'PRECTOTCORR': 'Lượng Mưa (mm/giờ)',
    'PS': 'Áp Suất Bề Mặt (kPa)',
    'T2M': 'Nhiệt Độ (°C)',
    'ALLSKY_SFC_PAR_TOT': 'Bức Xạ PAR (W m-2)'
}

for i, param in enumerate(thong_so):
    du_doan = Y_du_doan_nguyen[:, :, i][0]
    thuc_te = Y_kiem_tra_nguyen[:, :, i][0]

    plt.figure(figsize=(12, 6))
    plt.plot(thuc_te, label='Thực tế', marker='o', linestyle='dashed')
    plt.plot(du_doan, label='Dự đoán', marker='x', linestyle='solid')
    plt.title(f'Dự Báo {tieu_de[param]} Cho 24 Giờ Tiếp Theo')
    plt.xlabel('Giờ')
    plt.ylabel(tieu_de[param])
    plt.legend()
    plt.show()
