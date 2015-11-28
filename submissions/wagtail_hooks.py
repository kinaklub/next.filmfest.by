from django.conf.urls import include, url
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore import hooks
from wagtail.wagtailadmin.menu import MenuItem

from submissions import admin_urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^submissions/', include(admin_urls, namespace='submissions')),
    ]


class SubmissionsMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm('submissions.view_submission')


@hooks.register('register_admin_menu_item')
def register_submissions_menu_item():
    return SubmissionsMenuItem(
        _('Submissions'),
        urlresolvers.reverse('submissions:index'),
        name='submissions',
        classnames='icon icon-doc-full-inverse',
        order=250
    )
