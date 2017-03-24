# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('results', '0020_clear_jurymemberpage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jurymemberpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='jurymemberpage',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='resultsrelatedjurymember',
            name='jury_member',
        ),
        migrations.RemoveField(
            model_name='resultsrelatedjurymember',
            name='page',
        ),
        migrations.DeleteModel(
            name='JuryMemberPage',
        ),
        migrations.DeleteModel(
            name='ResultsRelatedJuryMember',
        ),
    ]
