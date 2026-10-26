from rest_framework.permissions import BasePermission
from accounts.models import UserProfile

class IsGestor(BasePermission):
    message = "Esta operação está disponível apenas para usuários com perfil Gestor."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            return request.user.profile.role == UserProfile.Role.GESTOR
        except UserProfile.DoesNotExist:
            return False
