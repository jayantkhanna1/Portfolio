# Generated by Django 3.2.6 on 2021-08-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_website_app', '0005_accomplishments'),
    ]

    operations = [
        migrations.AddField(
            model_name='accomplishments',
            name='url',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]