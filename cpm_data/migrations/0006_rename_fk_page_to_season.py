# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-10 13:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cpm_data', '0005_add_jury_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seasonrelatedjurymember',
            old_name='page',
            new_name='season',
        ),
        migrations.RenameField(
            model_name='seasonrelatedpartner',
            old_name='page',
            new_name='season',
        ),
    ]
