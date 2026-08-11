import firebase_admin
from firebase_admin import credentials, db


# Firebase Realtime Database URL
DATABASE_URL = "https://maternal-health-iot-default-rtdb.firebaseio.com/"


# Load Firebase service account
cred = credentials.Certificate("firebase_key.json")


# Initialize Firebase
firebase_admin.initialize_app(
    cred,
    {
        "databaseURL": DATABASE_URL
    }
)


def save_reading(patient_id, data):
    """
    Save the latest patient reading to Firebase.
    """

    ref = db.reference(f"patients/{patient_id}")

    ref.set(data)

    print(f"✅ Firebase updated for {patient_id}")