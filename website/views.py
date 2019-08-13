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
from .forms import CompanyForm, NewPasswordForm, EmailForm, ReviewForm, PlaceIDForm
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


class DashboardView(LoginRequiredMixin, FormView):
    template_name = 'website/dashboard.html'
    form_class = EmailForm

    def form_valid(self, form):
        company = Company.objects.get(user=self.request.user)
        company.send_email(form.cleaned_data['email'])
        return redirect(self.get_success_url())

    def get_success_url(self, *args, **kwargs):
        slug = Company.objects.get(user=self.request.user).slug
        return reverse_lazy('website:dashboard', kwargs={'slug':slug})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['company'] = Company.objects.get(user=self.request.user)
        return context


class ReviewPage(CreateView):
    template_name = 'website/review.html'
    form_class = ReviewForm
    success_url = reverse_lazy('website:thanks')

    def form_valid(self, form):
        company = Company.objects.get(slug=self.kwargs.get('slug'))
        self.object = form.save(commit=False)
        self.object.company = company
        self.object.save()
        return redirect(self.success_url)
    #
    # def get_context_data(self, *args, **kwargs):
    #     super().get_context_data(*args, **kwargs)
    #     context['company'] = self.request.kwargs.get('company')
    #     return context
    #

class ThanksPage(TemplateView):
    template_name = 'website/thanks.html'


class AskReview(TemplateView):
    template_name = 'website/ask_review.html'

    def get_context_data(self, **kwargs):
        company = Company.objects.get(slug=self.kwargs.get('slug'))
        context = {
            'company': company
        }
        return context


class CreateUser(FormView):
    template_name = 'website/set_password.html'
    form_class = NewPasswordForm

    def form_valid(self, form):
        company = Company.objects.get(slug=self.request.POST.get('slug'))
        password = form.cleaned_data['password']
        company.set_password(password)
        return redirect(reverse_lazy('website:set_place_id', kwargs={'slug': company.slug}))

    def get_context_data(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(*args, **kwargs)
        context['slug'] = slug
        return context


class SetPlaceID(FormView):
    template_name = 'website/set_place_id.html'
    form_class = PlaceIDForm

    def form_valid(self, form):
        company = Company.objects.get(slug=self.kwargs.get('slug'))
        company.place_id = form.cleaned_data['place_id']
        company.save()
        return redirect(reverse_lazy('website:dashboard', kwargs={'slug': company.slug}))
