from django.urls import path
from eBirth_auth.views import (
    DashboardView,
    LoginView,
    LogoutView,
)

app_name = "auth"

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name="dashboard"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]

