import firebase_admin
from firebase_admin import credentials, db

# Đường dẫn đến file JSON đã tải về
FIREBASE_KEY_PATH = "firebase-key.json"
FIREBASE_URL = "https://weather2-b2bc4-default-rtdb.firebaseio.com"  # Thay bằng URL thật của bạn

# Kiểm tra và khởi tạo Firebase nếu chưa có
if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_KEY_PATH)
    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_URL})

def get_firebase_reference(path):
    return db.reference(path)  # Trả về tham chiếu đến node Firebase
