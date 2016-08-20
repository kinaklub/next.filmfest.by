from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from cpm_data.models import JuryMember


class MyPageModelAdmin(ModelAdmin):
    model = JuryMember
    menu_label = 'Jury'
    menu_order = 200  # will put in 3rd place (000 being 1st, 100 2nd)
    list_display = ('name', 'country')
    search_fields = ('name_en', 'name_be', 'name_ru')


modeladmin_register(MyPageModelAdmin)
