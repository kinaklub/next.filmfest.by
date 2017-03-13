import pytest
from wagtail.tests.testapp.models import PageChooserModel
from wagtail.wagtailadmin.edit_handlers import ObjectList
from wagtail.wagtailcore.models import Page

from modeladminutils.edit_handlers import AdminModelChooserPanel


class TestAdminModelChooserPanel(object):
    @pytest.fixture
    def model(self):
        """A model with a foreign key to Page
        which we want to render as a page chooser
        """
        return PageChooserModel

    @pytest.fixture
    def edit_handler_class(self, model):
        """A AdminModelChooserPanel class that works on
        PageChooserModel's 'page' field
        """
        object_list = ObjectList([AdminModelChooserPanel('page')])
        return object_list.bind_to_model(model)

    @pytest.fixture
    def panel_class(self, edit_handler_class):
        return edit_handler_class.children[0]

    @pytest.fixture
    def form_class(self, model, edit_handler_class):
        """A form class containing the fields
        that MyPageChooserPanel wants
        """
        return edit_handler_class.get_form_class(model)

    @pytest.fixture
    def test_page(self):
        page = Page(
            title='testpage',
            slug='test',
            path='000100019999',
            depth=3
        )
        page.save()
        return page

    @pytest.fixture
    def test_instance(self, model, test_page):
        return model.objects.create(page=test_page)

    @pytest.fixture
    def test_form(self, form_class, test_instance):
        return form_class(instance=test_instance)

    @pytest.fixture
    def panel(self, panel_class, test_instance, test_form):
        return panel_class(instance=test_instance, form=test_form)

    @pytest.mark.django_db
    def test_render(self, panel, test_page):
        # when panel for test_instance is rendered as html
        field_html = panel.render_as_field()

        # then input with value=test_page.id is in the field HTML
        input_html = (
            '<input id="id_page" name="page" type="hidden" '
            'value="%s" />' % test_page.id
        )
        assert input_html in field_html
        # and createAdminModelChooser script is in the field HTML
        script_html = (
            '<script>'
            'createAdminModelChooser("id_page", "wagtailcore/page");'
            '</script>'
        )
        assert script_html in field_html
