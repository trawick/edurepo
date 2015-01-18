# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import resources.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('votes', models.IntegerField(default=0)),
                ('inappropriate_flags', models.IntegerField(default=0)),
                ('url', models.URLField(validators=[resources.models.validate_resource_url])),
                ('notes', models.CharField(max_length=1000, blank=True)),
                ('when_added', models.DateTimeField(auto_now_add=True)),
                ('objective', models.ForeignKey(to='repo.LearningObjective')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceSubmission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'c', max_length=1, choices=[(b'c', b'Creator'), (b'v', b'Voter'), (b'f', b'Flagger')])),
                ('comment', models.CharField(max_length=160, blank=True)),
                ('when', models.DateTimeField(auto_now_add=True)),
                ('resource', models.ForeignKey(to='resources.Resource')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResourceVerification',
            fields=[
                ('url', models.URLField(unique=True, serialize=False, primary_key=True)),
                ('last_success', models.DateTimeField(null=True, blank=True)),
                ('last_failure', models.DateTimeField(null=True, blank=True)),
                ('document_title', models.CharField(max_length=120, blank=True)),
                ('content_type', models.CharField(max_length=127, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='resourcesubmission',
            unique_together=set([('user', 'resource', 'type')]),
        ),
        migrations.AlterUniqueTogether(
            name='resource',
            unique_together=set([('objective', 'url')]),
        ),
    ]
