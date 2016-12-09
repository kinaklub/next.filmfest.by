from django.conf.urls import include, url
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core import urlresolvers
from django.utils.html import format_html

from wagtail.wagtailcore import hooks

from modeladminutils import admin_urls


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^genericmodel/', include(admin_urls,
                                       namespace='modeladminutils',
                                       app_name='modeladminutils')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script src="{0}"></script>
            <script>window.chooserUrls.genericmodelChooser = '{1}';</script>
        """,
        static('modeladminutils/js/genericmodel-chooser.js'),
        urlresolvers.reverse('modeladminutils:choose_generic')
    )
