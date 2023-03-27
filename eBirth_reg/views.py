from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from random import choice, randint, shuffle
from django.contrib import messages

# My App imports
from eBirth_reg.models import (
    HospitalAdminProfile,
    HospitalProfile,
    BirthRegistration,
)

from eBirth_auth.models import (
    User,
)

from eBirth_reg.forms import (
    BirthRegistrationForm
)

DEFAULT_PASSWORD = '12345678'

# Create your views here.

def _cert_no():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    cert_list = []

    [cert_list.append(choice(letters)) for _ in range(6)]
    [cert_list.append(choice(numbers)) for _ in range(4)]

    shuffle(list(cert_list))
    cert_no = ''.join(cert_list)

    return cert_no

def generate_cert_no():
    exists = True
    cert_no = None
    while exists:
        cert_no = _cert_no()
        if not User.objects.filter(cert_no=cert_no).exists():
            exists = False
    return cert_no

class BirthRegistrationView(SuccessMessageMixin, CreateView):
    model = BirthRegistration
    form_class = BirthRegistrationForm
    template_name = "auth/birth_reg.html"
    success_message = ""

    def get_success_url(self):
        return reverse("reg:birth_reg")

    def form_valid(self, form):

        admin_profile = HospitalAdminProfile.objects.filter(user_id=self.request.user)

        if admin_profile.exists():
            hospital = admin_profile[0].hospital_id
            cert_no = generate_cert_no()

            user_id = User.objects.create_user(password=DEFAULT_PASSWORD, cert_no=cert_no)

            form.instance.user_id = user_id
            form.instance.place_of_birth = hospital
            form.instance.certificate_num = cert_no

            self.success_message = f"Birth Registration Successful with certificate No: {cert_no}"

            return super().form_valid(form)

        else:
            messages.error(self.request, "Unable to get hospital profile!")
            return super().form_invalid(form)

