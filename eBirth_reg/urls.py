from django.urls import path

from eBirth_reg.views import (
    BirthRegistrationView,
    ManageBirthRegistrationView,
    EditBirthRegistrationView,
    DeleteBirthRegistrationView,

    AdminRegistrationView,
)

app_name = "reg"

urlpatterns = [
    path('birth_reg', BirthRegistrationView.as_view(), name="birth_reg"),
    path('manage_birth_reg', ManageBirthRegistrationView.as_view(), name="manage_birth_reg"),
    path('edit_birth_reg/<str:pk>', EditBirthRegistrationView.as_view(), name="edit_birth_reg"),
    path('delete_birth_reg/<str:pk>', DeleteBirthRegistrationView.as_view(), name="delete_birth_reg"),

    path('admin_reg', AdminRegistrationView.as_view(), name="admin_reg"),
]

