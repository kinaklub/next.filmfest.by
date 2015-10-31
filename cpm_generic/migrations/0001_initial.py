# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0019_verbose_names_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('caption_en', models.CharField(max_length=250)),
                ('caption_be', models.CharField(max_length=250)),
                ('caption_ru', models.CharField(max_length=250)),
                ('description_en', wagtail.wagtailcore.fields.RichTextField(default=b'')),
                ('description_be', wagtail.wagtailcore.fields.RichTextField(default=b'')),
                ('description_ru', wagtail.wagtailcore.fields.RichTextField(default=b'')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
