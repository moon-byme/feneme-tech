from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import UserProfile
from accounts.permissions import IsGestor
from accounts.serializers import FenemeTokenObtainPairSerializer

User = get_user_model()

class FenemeLoginView(TokenObtainPairView):
    serializer_class = FenemeTokenObtainPairSerializer

class DriverOptionSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]

class DriverListView(generics.ListAPIView):
    serializer_class = DriverOptionSerializer
    permission_classes = [IsAuthenticated, IsGestor]

    def get_queryset(self):
        return User.objects.filter(
            is_active=True,
            profile__role=UserProfile.Role.MOTORISTA,
        ).order_by("username")
