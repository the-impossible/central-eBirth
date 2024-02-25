from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


# My app imports

# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "auth/dashboard.html"

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')

    def post(self, request):
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user:
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"You are now signed in {user}")

                    nxt  = request.GET.get('next', None)
                    if nxt is None:
                        return redirect('auth:dashboard')
                    return redirect(self.request.GET.get('next', None))

                else:
                    messages.warning(request, 'Account not active contact the administrator')
            else:
                messages.error(request, 'Invalid login credentials')
        else:
            messages.error(request, 'All fields are required!!')
        return redirect('auth:login')

class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')
