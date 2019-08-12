from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
            # General Page Views
            url(r'^$', Redirect.as_view(), name='redirect'),
            url(r'^homepage/$', HomepageView.as_view(), name='homepage'),
            url(r'^dashboard/(?P<slug>[-\w]+)/$', DashboardView.as_view(), name='dashboard'),
            url(r'^set-password/(?P<slug>[-\w]+)/$', CreateUser.as_view(), name='set_password'),
            url(r'^review/$', ReviewPage.as_view(), name='review'),
            url(r'^ask_review/$', AskReview.as_view(), name='ask_review'),
]
