# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0029_unicode_slugfield_dj19'),
        ('wagtailredirects', '0005_capitalizeverbose'),
        ('wagtailforms', '0003_capitalizeverbose'),
        ('results', '0022_remove_film_page_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='filmpage',
            name='frame',
        ),
        migrations.RemoveField(
            model_name='filmpage',
            name='page_ptr',
        ),
        migrations.RemoveField(
            model_name='filmpage',
            name='submission',
        ),
        migrations.RemoveField(
            model_name='resultsrelatedwinner',
            name='film',
        ),
        migrations.RemoveField(
            model_name='resultsrelatedwinner',
            name='page',
        ),
        migrations.DeleteModel(
            name='FilmPage',
        ),
        migrations.DeleteModel(
            name='ResultsRelatedWinner',
        ),
    ]
