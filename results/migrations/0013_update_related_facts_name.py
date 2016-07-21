# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0012_add_winner_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultsfact',
            name='page',
            field=modelcluster.fields.ParentalKey(related_name='related_facts',
                                                  to='results.ResultsPage'),
        ),
    ]
