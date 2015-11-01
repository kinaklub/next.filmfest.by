import pytest


@pytest.mark.django_db
def test_add_subpage():
    from django.apps.registry import apps

    from cpm_generic.models import IndexPage
    from cpm_generic.migration_utils import add_subpage, get_content_type
    from home.models import HomePage

    index_page_ct = get_content_type(apps, 'cpm_generic', 'indexpage')

    homepage = HomePage.objects.get(slug='home')
    indexpage = add_subpage(
        parent=homepage,
        model=IndexPage,
        title='title',
        slug='slug',
        caption_en='caption_en',
        caption_be='caption_be',
        caption_ru='caption_ru',
        description_en='description_en',
        description_be='description_en',
        description_ru='description_ru',
        content_type=index_page_ct,
    )

    assert indexpage.caption_en == 'caption_en'
    assert indexpage.get_parent().path == homepage.path


@pytest.mark.django_db
def test_get_content_type():
    from django.apps.registry import apps

    from cpm_generic.migration_utils import get_content_type

    # testing new content type
    content_type = get_content_type(apps, 'app', 'Model')
    assert content_type.app_label == 'app'
    assert content_type.model == 'Model'

    # testing existing content type
    content_type = get_content_type(apps, 'app', 'Model')
    assert content_type.app_label == 'app'
    assert content_type.model == 'Model'
