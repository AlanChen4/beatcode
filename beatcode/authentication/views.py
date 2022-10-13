from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    fields = '__all__'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)


class RegisterPage(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)    

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().get(*args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'first_name', 'last_name']
    template_name = 'authentication/profile.html'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            return redirect('home')
        return super().form_valid(form)

    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)
