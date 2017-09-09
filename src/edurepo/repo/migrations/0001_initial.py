# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import repo.models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=30, unique=True, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[A-Za-z0-9-]*$', message=b'Course ids may contain only letters, numbers, and hyphens.')])),
                ('description', models.CharField(max_length=4000)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CourseCategory',
            fields=[
                ('id', models.CharField(max_length=8, unique=True, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[A-Za-z0-9-]*$', message=b'Course category ids may contain only letters, numbers, and hyphens.')])),
                ('description', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'course categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlossaryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=60)),
                ('definition', models.CharField(max_length=4096)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ICan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.CharField(max_length=200)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LearningObjective',
            fields=[
                ('id', models.CharField(max_length=40, unique=True, serialize=False, primary_key=True, validators=[django.core.validators.RegexValidator(regex=b'^[A-Za-z0-9-\\.]*$', message=b'Learning objective ids may contain only letters, numbers, hyphens, and periods.')])),
                ('description', models.CharField(max_length=4096)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleChoiceItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=400)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
                ('choice1', models.CharField(max_length=200)),
                ('choice2', models.CharField(max_length=200)),
                ('choice3', models.CharField(max_length=200, blank=True)),
                ('choice4', models.CharField(max_length=200, blank=True)),
                ('choice5', models.CharField(max_length=200, blank=True)),
                ('type', models.CharField(max_length=1, choices=[(b'1', b'One of the provided answers is the only correct answer in the universe.'), (b'2', b'Only one of the provided answers is correct, but there may be more correct answers in the universe.'), (b'3', b'None of the provided answers is correct.')])),
                ('ans', models.PositiveSmallIntegerField(choices=[(1, b'The 1st answer is the correct choice.'), (2, b'The 2nd answer is the correct choice.'), (3, b'The 3rd answer is the correct choice.'), (4, b'The 4th answer is the correct choice.'), (5, b'The 5th answer is the correct choice.')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReferenceText',
            fields=[
                ('learning_objective', models.ForeignKey(primary_key=True, serialize=False, to='repo.LearningObjective', unique=True, on_delete=models.CASCADE)),
                ('text', models.CharField(max_length=4000)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrueFalseItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('statement', models.CharField(max_length=1024)),
                ('answer', models.BooleanField(default=None)),
                ('language', repo.models.RepoLanguageField(default=b'en', max_length=8, blank=True, choices=[(b'en', b'English'), (b'es', b'Spanish')])),
                ('learning_objective', models.ForeignKey(to='repo.LearningObjective', on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='multiplechoiceitem',
            name='learning_objective',
            field=models.ForeignKey(to='repo.LearningObjective', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='learningobjective',
            name='course',
            field=models.ForeignKey(to='repo.Course', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ican',
            name='learning_objective',
            field=models.ForeignKey(to='repo.LearningObjective', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='glossaryitem',
            name='learning_objective',
            field=models.ForeignKey(to='repo.LearningObjective', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='glossaryitem',
            unique_together=set([('term', 'learning_objective')]),
        ),
        migrations.AddField(
            model_name='course',
            name='cat',
            field=models.ForeignKey(to='repo.CourseCategory', on_delete=models.CASCADE),
            preserve_default=True,
        ),
    ]
