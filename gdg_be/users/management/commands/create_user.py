from django.core.management.base import BaseCommand

import firebase_admin
from firebase_admin import credentials, auth


class Command(BaseCommand):
    help = "Create a user"

    def handle(self, *args, **options):

        # Provide a test email
        email = "testuser1@example.com"
        display_name = "Test User"

        # Step 1: Create or get the user
        try:
            user = auth.get_user_by_email(email)
            print(f"User found: {user.uid}")
        except auth.UserNotFoundError:
            user = auth.create_user(email=email, display_name=display_name)
            print(f"User created: {user.uid}")

        # Step 2: Create a custom token (JWT)
        custom_token = auth.create_custom_token(user.uid)

        # Step 3: Decode to UTF-8 string
        custom_token_str = custom_token.decode("utf-8")

        # 🔥 Paste this token in Postman request to get the ID token
        print("Firebase Custom Token:\n")
        print(custom_token_str)
