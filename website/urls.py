from django.conf.urls import url, include

from .views import *

# Application Routes (URLs)

app_name = 'website'

urlpatterns = [
            # General Page Views
            url(r'^$', Redirect.as_view(), name='redirect'),
            url(r'^homepage/$', HomepageView.as_view(), name='homepage'),
            url(r'^dashboard/(?P<slug>[-\w]+)/$', DashboardView.as_view(), name = 'dashboard'),
            url(r'^set-password/(?P<slug>[-\w]+)/$', CreateUser.as_view(), name = 'set_password'),
            url(r'^set-place-id/(?P<slug>[-\w]+)/$', SetPlaceID.as_view(), name = 'set_place_id'),
            url(r'^review/(?P<slug>[-\w]+)/$', ReviewPage.as_view(), name='review'),
            url(r'^ask-review/(?P<slug>[-\w]+)$', AskReview.as_view(), name='ask_review'),
            url(r'^thanks/$', ThanksPage.as_view(), name='thanks'),
]
