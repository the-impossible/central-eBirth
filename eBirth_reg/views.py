from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from random import choice, randint, shuffle
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin


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
    ChangePassForm,
)

from eBirth_reg.forms import (
    BirthRegistrationForm,
    HospitalProfileForm,
)

DEFAULT_PASSWORD = '12345678'

# Create your views here.


def _cert_no():
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    cert_list = ['M', 'H', 'S', '-']

    [cert_list.append(choice(letters)) for _ in range(3)]
    [cert_list.append(choice(numbers)) for _ in range(3)]

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


class BirthRegistrationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = BirthRegistration
    form_class = BirthRegistrationForm
    template_name = "auth/birth_reg.html"
    success_message = ""

    def get_success_url(self):
        return reverse("reg:birth_reg")

    def form_valid(self, form):

        admin_profile = HospitalAdminProfile.objects.filter(
            user_id=self.request.user)

        if admin_profile.exists():
            hospital = admin_profile[0].hospital_id
            cert_no = generate_cert_no()

            user_id = User.objects.create_user(
                password=DEFAULT_PASSWORD, cert_no=cert_no)

            form.instance.user_id = user_id
            form.instance.place_of_birth = hospital
            form.instance.certificate_num = cert_no

            self.success_message = f"Birth Registration Successful with certificate No: {cert_no}"

            return super().form_valid(form)

        else:
            messages.error(self.request, "Unable to get hospital profile!")
            return super().form_invalid(form)


class ManageBirthRegistrationView(LoginRequiredMixin, ListView):
    template_name = "auth/manage_reg.html"

    def get_queryset(self):
        try:
            hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
            queryset = BirthRegistration.objects.filter(place_of_birth=hospital)
            return queryset
        except HospitalAdminProfile.DoesNotExist:
            messages.error(self.request, "Contact Central e-Birth, hospital profile has not been fully updated!!, therefore birth-registration list can't be displayed")
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('auth:dashboard'))
        return super().get(request, *args, **kwargs)


class EditBirthRegistrationView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = BirthRegistration
    form_class = BirthRegistrationForm
    success_message = "Registration has been edited successfully!"

    template_name = "auth/edit_birth_reg.html"

    def get_success_url(self):
        return reverse("reg:manage_birth_reg")


class DeleteBirthRegistrationView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = BirthRegistration
    success_message = "Registration has been deleted successfully!"

    def form_valid(self, form):
        user = User.objects.get(cert_no=self.request.POST.get('cert_no'))
        user.delete()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse("reg:manage_birth_reg")


class AdminRegistrationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "auth/admin_reg.html"
    success_message = "Admin Account created!"

    def get_success_url(self):
        return reverse("reg:admin_reg")

    def form_valid(self, form):
        form.instance.is_hospital_admin = True

        try:
            hospital = HospitalAdminProfile.objects.get(
                user_id=self.request.user).hospital_id

            form = super().form_valid(form)
            
            HospitalAdminProfile.objects.create(
                user_id=self.object, hospital_id=hospital)


            return form
        except HospitalAdminProfile.DoesNotExist:

            messages.error(
                self.request, "Contact Central e-Birth, hospital profile has not been updated!!")
            return redirect('auth:dashboard')


class ManageAdministratorsView(LoginRequiredMixin, ListView):
    template_name = "auth/manage_admin.html"

    def get_queryset(self):
        try:
            hospital = HospitalAdminProfile.objects.get(user_id=self.request.user).hospital_id
            queryset = HospitalAdminProfile.objects.filter(hospital_id=hospital).exclude(user_id=self.request.user)
            return queryset
        except HospitalAdminProfile.DoesNotExist:
            messages.error(self.request, "Contact Central e-Birth, hospital profile has not been fully updated!!, therefore admin list can't be displayed")
            return None

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('auth:dashboard'))
        return super().get(request, *args, **kwargs)


class DeleteAdministratorView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_message = "Administrator has been deleted!"

    def get_success_url(self):
        return reverse("reg:manage_admin")


class EditAdminView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditAdminForm
    success_message = "Admin account has been edited successfully!"

    template_name = "auth/edit_admin.html"

    def get_success_url(self):
        return reverse("reg:manage_admin")


class CertificateView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = BirthRegistration

    template_name = "auth/view_certificate.html"

    def get_object(self):
        try:
            return BirthRegistration.objects.get(birth_id=self.kwargs['pk'])
        except BirthRegistration.DoesNotExist:
            try:
                return BirthRegistration.objects.get(user_id=self.kwargs['pk'])
            except BirthRegistration.DoesNotExist:
                raise Http404()

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            messages.error(self.request, "Failed in getting certificate!")
            return redirect('auth:dashboard')

        return self.render_to_response(self.get_context_data())


class EditHospitalProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = HospitalProfile
    form_class = HospitalProfileForm
    success_message = "Hospital profile has been updated successfully!"
    hospital_id = None

    template_name = "auth/hospital_profile.html"

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except HospitalProfile.DoesNotExist:
            messages.error(
                self.request, "Contact Central e-Birth, hospital profile has not been updated!!")
            return redirect('auth:dashboard')

        return self.render_to_response(self.get_context_data())

    def get_object(self):
        return HospitalProfile.objects.get(hospital_id=HospitalProfile.objects.get(user_id=self.kwargs['pk']).hospital_id)


class AccountProfileView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = EditAdminForm
    success_message = "Account has been updated successfully!"

    template_name = "auth/account_profile.html"


class SearchCertificateView(LoginRequiredMixin, ListView):
    model = BirthRegistration
    template_name = "auth/certificate_search.html"

    def get_queryset(self):
        qs = self.request.GET.get('qs')
        place_of_birth = HospitalProfile.objects.get(
            user_id=self.request.user.user_id)
        result = (
            BirthRegistration.objects.filter(certificate_num=qs, place_of_birth=place_of_birth) |
            BirthRegistration.objects.filter(child_name__icontains=qs, place_of_birth=place_of_birth) |
            BirthRegistration.objects.filter(father_name__icontains=qs, place_of_birth=place_of_birth) |
            BirthRegistration.objects.filter(mother_name__icontains=qs, place_of_birth=place_of_birth) |
            BirthRegistration.objects.filter(
                date_time__icontains=qs, place_of_birth=place_of_birth)
        )
        return result

    def get_context_data(self, **kwargs):
        context = super(SearchCertificateView, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('qs')
        return context


class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = ChangePassForm
    success_message = "password has been updated successfully!"
    template_name = "auth/change_password.html"

    def form_valid(self, form):
        old_pass = form.cleaned_data.get('old_pass')
        user_pass = self.request.user.password

        if check_password(old_pass, user_pass):
            form.instance.set_password(form.cleaned_data.get('new_pass'))
            return super().form_valid(form)

        messages.error(self.request, "Incorrect current password!")
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse("auth:login")
