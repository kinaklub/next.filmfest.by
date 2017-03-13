from django.core.urlresolvers import NoReverseMatch, reverse

from wagtail.contrib.modeladmin.helpers import AdminURLHelper


def get_edit_url(model, object_id):
    """Get admin edit URL to an object of a model registered in ModelAdmin"""

    url_name = AdminURLHelper(model).get_action_url_name('edit')
    try:
        return reverse(url_name, args=[object_id])
    except NoReverseMatch:
        return None
