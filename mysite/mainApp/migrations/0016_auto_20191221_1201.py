# Generated by Django 2.2.6 on 2019-12-21 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0015_remove_comment_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='message',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='author',
            new_name='name',
        ),
    ]