# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0008_image_created_at_index'),
        ('submissions', '0001_initial'),
        ('wagtailcore', '0019_verbose_names_cleanup'),
        ('results', '0003_jurymemberpage_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilmPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),  # noqa
                ('film_title_en', models.CharField(default='', max_length=1000)),  # noqa
                ('film_title_be', models.CharField(default='', max_length=1000)),  # noqa
                ('film_title_ru', models.CharField(default='', max_length=1000)),  # noqa
                ('director_en', models.CharField(default='', max_length=1000)),
                ('director_be', models.CharField(default='', max_length=1000)),
                ('director_ru', models.CharField(default='', max_length=1000)),
                ('genre_en', models.CharField(default='', max_length=1000)),
                ('genre_be', models.CharField(default='', max_length=1000)),
                ('genre_ru', models.CharField(default='', max_length=1000)),
                ('synopsis_short_en', wagtail.wagtailcore.fields.RichTextField(default='')),  # noqa
                ('synopsis_short_be', wagtail.wagtailcore.fields.RichTextField(default='')),  # noqa
                ('synopsis_short_ru', wagtail.wagtailcore.fields.RichTextField(default='')),  # noqa
                ('synopsis_en', wagtail.wagtailcore.fields.RichTextField(default='')),  # noqa
                ('synopsis_be', wagtail.wagtailcore.fields.RichTextField(default='')),  # noqa
                ('synopsis_ru', wagtail.wagtailcore.fields.RichTextField(default='')),  # noqa
                ('frame', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='wagtailimages.Image', null=True)),  # noqa
                ('submission', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='submissions.Submission', null=True)),  # noqa
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
