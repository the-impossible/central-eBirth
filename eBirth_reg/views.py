from django.shortcuts import render, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
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
from eBirth_auth.forms import (
    UserRegistrationForm,
    EditAdminForm,
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

class ManageBirthRegistrationView(ListView):
    template_name = "auth/manage_reg.html"

    def get_queryset(self):
        hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
        return BirthRegistration.objects.filter(place_of_birth=hospital)

class EditBirthRegistrationView(SuccessMessageMixin, UpdateView):
    model = BirthRegistration
    form_class = BirthRegistrationForm
    success_message = "Registration has been edited successfully!"

    template_name = "auth/edit_birth_reg.html"

    def get_success_url(self):
        return reverse("reg:manage_birth_reg")

class DeleteBirthRegistrationView(SuccessMessageMixin, DeleteView):
    model = BirthRegistration
    success_message = "Registration has been deleted successfully!"

    def form_valid(self, form):
        user = User.objects.get(cert_no=self.request.POST.get('cert_no'))
        user.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("reg:manage_birth_reg")

class AdminRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "auth/admin_reg.html"
    success_message = "Admin Account created!"

    def get_success_url(self):
        return reverse("reg:admin_reg")

    def form_valid(self, form):
        form.instance.is_hospital_admin = True
        form = super().form_valid(form)

        hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
        HospitalAdminProfile.objects.create(user_id=self.object, hospital_id=hospital)

        return form

class ManageAdministratorsView(ListView):
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
        return HospitalAdminProfile.objects.filter(hospital_id=hospital)

class DeleteAdministratorView(SuccessMessageMixin, DeleteView):
    model = User
    success_message = "Administrator has been deleted!"

    def get_success_url(self):
        return reverse("reg:manage_admin")

class EditAdminView(SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditAdminForm
    success_message = "Admin account has been edited successfully!"

    template_name = "auth/edit_admin.html"

    def get_success_url(self):
        return reverse("reg:manage_admin")

