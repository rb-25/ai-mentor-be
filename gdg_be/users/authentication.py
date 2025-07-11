from firebase_admin import auth as firebase_auth, exceptions
from rest_framework import authentication, exceptions as drf_exceptions
from django.contrib.auth import get_user_model

User = get_user_model()


class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        id_token = auth_header.split("Bearer ")[1]

        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
        except (
            firebase_auth.InvalidIdTokenError,
            firebase_auth.ExpiredIdTokenError,
            exceptions.FirebaseError,
        ):
            raise drf_exceptions.AuthenticationFailed("Invalid Firebase ID token")

        uid = decoded_token.get("uid")
        email = decoded_token.get("email")
        name = decoded_token.get("name", "")
        print(name)

        if not email:
            raise drf_exceptions.AuthenticationFailed("No email in Firebase token")

        if not User.objects.filter(email=email).exists():
            user = User.objects.create(email=email, name=name)
            user.save()
            print("User created:", user)
        else:
            user = User.objects.get(email=email)

        return (user, None)
