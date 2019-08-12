from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import login, authenticate
from .models import Company
from .forms import CompanyForm, NewPasswordForm
import json

# -------------------------------------------------------------------------------
# Page Views
# -------------------------------------------------------------------------------

class Redirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            company = Company.objects.get(user=self.request.user).slug
            return reverse_lazy('website:dashboard', kwargs={'slug': company})
        return reverse_lazy('website:homepage')

class HomepageView(CreateView):
    template_name = 'website/homepage.html'
    form_class = CompanyForm

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('website:set_password', kwargs={'slug': self.object.slug})


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'website/dashboard.html'


class ReviewPage(TemplateView):
    template_name = 'website/review.html'


class AskReview(TemplateView):
    template_name = 'website/ask_review.html'


class CreateUser(FormView):
    template_name = 'website/set_password.html'
    form_class = NewPasswordForm

    def form_valid(self, form):
        company = Company.objects.get(slug=self.request.POST.get('slug'))
        password = form.cleaned_data['password']
        company.set_password(password)
        return redirect(reverse_lazy('website:dashboard', kwargs={'slug': company.slug}))

    def get_context_data(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(*args, **kwargs)
        context['slug'] = slug
        return context
