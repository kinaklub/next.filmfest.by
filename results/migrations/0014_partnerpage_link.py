# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0013_update_related_facts_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerpage',
            name='link',
            field=models.CharField(default='', max_length=250, blank=True),
        ),
    ]
