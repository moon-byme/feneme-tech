from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import DriverListView, FenemeLoginView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/login/", FenemeLoginView.as_view(), name="login"),
    path("api/auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/drivers/", DriverListView.as_view(), name="driver-list"),
    path("api/", include("deliveries.urls")),
]
