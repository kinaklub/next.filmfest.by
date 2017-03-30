from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from events.models import Venue


class VenueModelAdmin(ModelAdmin):
    model = Venue
    menu_label = 'Venues'
    menu_icon = 'site'
    menu_order = 270
    list_display = ('name_en', 'name_be', 'name_ru')
    search_fields = ('name_en', 'name_be', 'name_ru')


modeladmin_register(VenueModelAdmin)
