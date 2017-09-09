# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('objective', models.CharField(max_length=40)),
                ('comments', models.CharField(max_length=300, blank=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('email', models.EmailField(max_length=75, unique=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeacherClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('course_id', models.CharField(max_length=30)),
                ('repo_provider', models.CharField(max_length=250)),
                ('teacher', models.ForeignKey(to='teachers.Teacher', on_delete=models.CASCADE)),
            ],
            options={
                'verbose_name_plural': 'classes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='teacherclass',
            unique_together=set([('name', 'teacher')]),
        ),
        migrations.AddField(
            model_name='entry',
            name='teacher',
            field=models.ForeignKey(to='teachers.Teacher', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='teacher_class',
            field=models.ForeignKey(to='teachers.TeacherClass', on_delete=models.CASCADE),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='entry',
            unique_together=set([('teacher_class', 'date', 'objective')]),
        ),
    ]
