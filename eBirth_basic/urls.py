from django.urls import path
from eBirth_basic.views import HomeView

app_name = "basic"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]

