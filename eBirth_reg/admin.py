from django.contrib import admin

from eBirth_reg.models import (
    BirthRegistration,
    Gender,
    HospitalAdminProfile,
    HospitalProfile,
)

# Register your models here.
admin.site.register(BirthRegistration)
admin.site.register(Gender)
admin.site.register(HospitalAdminProfile)
admin.site.register(HospitalProfile)