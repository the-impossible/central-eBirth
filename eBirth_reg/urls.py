from django.urls import path

from eBirth_reg.views import (
    BirthRegistrationView,

)

app_name = "reg"

urlpatterns = [
    path('birth_reg', BirthRegistrationView.as_view(), name="birth_reg"),
]

