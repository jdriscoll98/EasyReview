from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q


class Company(models.Model):
    user = models.ForeignKey(User, blank=True,  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    company_name = models.CharField(max_length=100)
    place_id = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.company_name

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save_user(self, *args, **kwargs):
        slug = slugify(self.company_name)
        self.slug = slug
        user = User(username=slug)
        user.save()
        self.user = user
        super(Company, self).save(*args, **kwargs)

    def set_password(self, password):
        user = self.user
        user.set_password(password)
        user.save()

    def send_email(self, email):
        subject = 'How was your experience with {}?'.format(self.company_name)
        link = reverse('website:review', kwargs={'slug': self.slug})
        html_message = render_to_string('website/mail_template.html', context = {'company': self.company_name, 'link':link})
        plain_message = strip_tags(html_message)
        from_email = self.email
        to = email
        send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        print('sent')

    def get_pending_customers(self):
        return Review.objects.filter(Q(company=self) & ~Q(email=None))



class Review(models.Model):
    reasons = (
        ('Poor Service', 'Poor Service'),
        ('Too Expensive', 'Too Expensive'),
        ('Other', 'Other')
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reason = models.CharField(choices=reasons, max_length=100)
    review = models.TextField(max_length=1000)

    def __str__(self):
        return self.reason
