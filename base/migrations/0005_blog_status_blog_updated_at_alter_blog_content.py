# Generated by Django 5.1.2 on 2024-10-29 15:40

import ckeditor.fields
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_remove_blog_status_remove_blog_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default=django.utils.timezone.now, max_length=7),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='blog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
