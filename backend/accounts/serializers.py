from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from accounts.models import UserProfile

class FenemeTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            token["role"] = user.profile.role
        except UserProfile.DoesNotExist:
            token["role"] = UserProfile.Role.MOTORISTA
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        try:
            role = self.user.profile.role
        except UserProfile.DoesNotExist:
            role = UserProfile.Role.MOTORISTA
        data["user"] = {
            "id": self.user.id,
            "username": self.user.get_username(),
            "role": role,
        }
        return data
