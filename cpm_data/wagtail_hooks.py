from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from cpm_data.models import JuryMember, Partner, Season


class SeasonModelAdmin(ModelAdmin):
    model = Season
    menu_label = 'Seasons'
    menu_icon = 'date'
    menu_order = 200
    list_display = ('name_en', 'name_be', 'name_ru')
    search_fields = ('name_en', 'name_be', 'name_ru')


class JuryMemberModelAdmin(ModelAdmin):
    model = JuryMember
    menu_label = 'Jury'
    menu_icon = 'group'
    menu_order = 210
    list_display = ('name_en', 'name_be', 'name_ru', 'country')
    search_fields = ('name_en', 'name_be', 'name_ru')


class PartnerModelAdmin(ModelAdmin):
    model = Partner
    menu_label = 'Partners'
    menu_icon = 'grip'
    menu_order = 220
    list_display = ('name_en', 'name_be', 'name_ru', 'image')
    search_fields = ('name_en', 'name_be', 'name_ru')


modeladmin_register(SeasonModelAdmin)
modeladmin_register(JuryMemberModelAdmin)
modeladmin_register(PartnerModelAdmin)
