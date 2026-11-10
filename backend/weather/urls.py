from django.urls import path

from weather.views import DailyForecastView, ReferenceLocationListView

urlpatterns = [
    path("weather/locations/", ReferenceLocationListView.as_view(), name="weather-locations"),
    path("weather/forecast/", DailyForecastView.as_view(), name="weather-forecast"),
]
