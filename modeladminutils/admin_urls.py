from django.conf.urls import url

from modeladminutils.views import chooser

urlpatterns = [
    url(r'^choose/$', chooser.choose, name='choose_generic'),
    url(r'^choose/(\w+)/(\w+)/$', chooser.choose, name='chooser'),
    url(r'^choose/(\w+)/(\w+)/(\d+)/$', chooser.chosen, name='chosen'),
]
