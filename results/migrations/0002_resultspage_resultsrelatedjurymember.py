# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultsPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('caption_en', models.CharField(max_length=250)),
                ('caption_be', models.CharField(max_length=250)),
                ('caption_ru', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='ResultsRelatedJuryMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('jury_member', models.ForeignKey(related_name='+', blank=True, to='results.JuryMemberPage', null=True)),
                ('page', modelcluster.fields.ParentalKey(related_name='related_jury_members', to='results.ResultsPage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
    ]
