# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import chain

from django.db import migrations

from cpm_generic.migration_utils import (add_subpage, remove_subpage,
                                         get_content_type)


def _add_year_results(apps, page_kwargs, jury_members):
    HomePage = apps.get_model('home.HomePage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")
    RelatedJuryMember = apps.get_model('results.ResultsRelatedJuryMember')
    ResultsPage = apps.get_model('results.ResultsPage')

    results_page_ct = get_content_type(apps, 'results', 'resultspage')

    homepage = HomePage.objects.get(slug='home')
    results12_page = add_subpage(
        homepage,
        ResultsPage,
        content_type=results_page_ct,
        **page_kwargs
    )

    RelatedJuryMember.objects.bulk_create(
        [
            RelatedJuryMember(
                sort_order=index,
                jury_member=JuryMemberPage.objects.get(title=title),
                page=results12_page,
            ) for index, title in enumerate(jury_members)
        ]
    )


def _remove_year_results(apps, page_kwargs, jury_members):
    HomePage = apps.get_model('home.HomePage')
    JuryMemberPage = apps.get_model("results.JuryMemberPage")
    RelatedJuryMember = apps.get_model('results.ResultsRelatedJuryMember')
    ResultsPage = apps.get_model('results.ResultsPage')

    results_page_ct = get_content_type(apps, 'results', 'resultspage')

    homepage = HomePage.objects.get(slug='home')
    results12_page = remove_subpage(
        homepage,
        ResultsPage,
        content_type=results_page_ct,
        **page_kwargs
    )

    related_jury_ids = chain.from_iterable(
        RelatedJuryMember.objects.filter(
            jury_member=JuryMemberPage.objects.get(title=title),
            page=results12_page,
        ).values_list('id', flat=True) for title in jury_members
    )
    RelatedJuryMember.objects.filter(id__in=related_jury_ids).delete()


def _get_data_2012():
    page_kwargs = dict(
        title=u'Results 2012',
        slug='results2012',
        caption_en='2012: how it was',
        caption_be='2012: як гэта было',
        caption_ru='2012: как это было',
    )
    jury_members = [
        'Cory McAbee', 'Bohdana Smirnova', 'Sergey Krasikov',
        'Andrew Kureichik', 'Yuri Igrusha', 'Pavel Ivanov',
        'Maciej Gil', 'Victor Aslyuk', 'Agricola de Cologne',
    ]
    return page_kwargs, jury_members


def add_results_2012(apps, schema_editor):
    page_kwargs, jury_members = _get_data_2012()
    _add_year_results(apps, page_kwargs, jury_members)


def remove_results_2012(apps, schema_editor):
    page_kwargs, jury_members = _get_data_2012()
    _remove_year_results(apps, page_kwargs, jury_members)


def _get_data_2013():
    page_kwargs = dict(
        title=u'Results 2013',
        slug='results2013',
        caption_en='2013: good memories',
        caption_be='2013: добрыя ўспаміны',
        caption_ru='2013: хорошие воспоминания',
    )
    jury_members = [
        'Cory McAbee', 'Lee Sang-woo', 'Karsten Weber',
        'Pierre-Luc Vaillancourt', 'Maciej Gil', 'Jon Rubin',
        'Bohdana Smirnova', 'Sergey Krasikov', 'Yuri Igrusha',
        'Pavel Ivanov', 'Anton Sidorenko', 'Irina Demyanova',
        'Volha Dashuk',
    ]
    return page_kwargs, jury_members


def add_results_2013(apps, schema_editor):
    page_kwargs, jury_members = _get_data_2013()
    _add_year_results(apps, page_kwargs, jury_members)


def remove_results_2013(apps, schema_editor):
    page_kwargs, jury_members = _get_data_2013()
    _remove_year_results(apps, page_kwargs, jury_members)


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_add_jury_data'),
    ]

    operations = [
        migrations.RunPython(add_results_2012, remove_results_2012),
        migrations.RunPython(add_results_2013, remove_results_2013),
    ]
