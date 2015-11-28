from django.conf.urls import url

from submissions import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<submission_id>\d+)/$', views.details, name='details'),
]
