# Generated by Django 3.2.6 on 2021-10-06 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_website_app', '0012_animations_fullstack_website_static_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='animations',
            name='sheetname',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fullstack_website',
            name='sheetname',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='static_website',
            name='sheetname',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='static_website',
            name='img',
            field=models.ImageField(null=0, upload_to='pics/static_website/'),
        ),
    ]