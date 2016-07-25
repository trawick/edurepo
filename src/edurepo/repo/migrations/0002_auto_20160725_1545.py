# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referencetext',
            name='learning_objective',
            field=models.OneToOneField(primary_key=True, serialize=False, to='repo.LearningObjective'),
        ),
    ]
