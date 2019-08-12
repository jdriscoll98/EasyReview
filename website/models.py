from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Company(models.Model):
    user = models.ForeignKey(User, blank=True,  on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    company_name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)

    def __str__(self):
        return self.company_name

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
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


class Review(models.Model):
    reasons = (
        ('Poor Service', 'Poor Service'),
        ('Too Expensive', 'Too Expensive'),
        ('Other', 'Other')
    )
    name = models.CharField(max_length=100, blank=True, default="Anonymous")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reason = models.CharField(choices=reasons, max_length=100)
    review = models.CharField(max_length=1000)

    def __str__(self):
        return self.reason
