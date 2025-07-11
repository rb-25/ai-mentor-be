import firebase_admin
from firebase_admin import credentials, auth, firestore, db, storage
from django.conf import settings
import os


def initialize_firebase_admin():
    try:
        cred_path = "gdg-be-firebase-adminsdk-fbsvc-b11cec50cc.json"
        if not os.path.exists(cred_path):
            raise FileNotFoundError(
                f"Firebase credentials file not found at: {cred_path}"
            )

        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized successfully!")

    except Exception as e:
        print(f"Error initializing Firebase Admin SDK: {e}")
        # Handle the error appropriately, perhaps log it or exit
