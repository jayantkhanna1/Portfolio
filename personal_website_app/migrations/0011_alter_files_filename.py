# Generated by Django 3.2.6 on 2021-10-03 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_website_app', '0010_alter_files_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='filename',
            field=models.CharField(max_length=9000),
        ),
    ]