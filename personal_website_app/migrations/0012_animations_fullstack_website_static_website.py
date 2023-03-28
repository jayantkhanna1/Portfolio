# Generated by Django 3.2.6 on 2021-10-05 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_website_app', '0011_alter_files_filename'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('desc', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=200)),
                ('startdate', models.CharField(max_length=100)),
                ('enddate', models.CharField(max_length=100)),
                ('likes', models.IntegerField()),
                ('img', models.ImageField(null=0, upload_to='pics/animations/')),
            ],
        ),
        migrations.CreateModel(
            name='Fullstack_website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('desc', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=200)),
                ('startdate', models.CharField(max_length=100)),
                ('enddate', models.CharField(max_length=100)),
                ('likes', models.IntegerField()),
                ('img', models.ImageField(null=0, upload_to='pics/dynamic/')),
            ],
        ),
        migrations.CreateModel(
            name='Static_website',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('desc', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=200)),
                ('startdate', models.CharField(max_length=100)),
                ('enddate', models.CharField(max_length=100)),
                ('likes', models.IntegerField()),
                ('img', models.ImageField(null=0, upload_to='pics/static/')),
            ],
        ),
    ]