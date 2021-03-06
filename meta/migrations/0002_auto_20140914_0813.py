# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meta', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='country',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='image',
            name='caption_en',
        ),
        migrations.RemoveField(
            model_name='image',
            name='caption_pt',
        ),
        migrations.RemoveField(
            model_name='image',
            name='notes_en',
        ),
        migrations.RemoveField(
            model_name='image',
            name='notes_pt',
        ),
        migrations.RemoveField(
            model_name='image',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='image',
            name='title_pt',
        ),
        migrations.RemoveField(
            model_name='size',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='size',
            name='description_pt',
        ),
        migrations.RemoveField(
            model_name='size',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='size',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='description_pt',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='tagcategory',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='tagcategory',
            name='description_pt',
        ),
        migrations.RemoveField(
            model_name='tagcategory',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='tagcategory',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='taxon',
            name='common_en',
        ),
        migrations.RemoveField(
            model_name='taxon',
            name='common_pt',
        ),
        migrations.RemoveField(
            model_name='taxon',
            name='rank_en',
        ),
        migrations.RemoveField(
            model_name='taxon',
            name='rank_pt',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='description_en',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='description_pt',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='name_en',
        ),
        migrations.RemoveField(
            model_name='tour',
            name='name_pt',
        ),
        migrations.RemoveField(
            model_name='video',
            name='caption_en',
        ),
        migrations.RemoveField(
            model_name='video',
            name='caption_pt',
        ),
        migrations.RemoveField(
            model_name='video',
            name='notes_en',
        ),
        migrations.RemoveField(
            model_name='video',
            name='notes_pt',
        ),
        migrations.RemoveField(
            model_name='video',
            name='title_en',
        ),
        migrations.RemoveField(
            model_name='video',
            name='title_pt',
        ),
    ]
