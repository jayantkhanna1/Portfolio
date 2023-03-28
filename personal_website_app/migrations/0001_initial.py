# Generated by Django 3.2.6 on 2021-08-24 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('year_from', models.CharField(max_length=20)),
                ('year_too', models.CharField(max_length=20)),
                ('per_got', models.CharField(max_length=30)),
                ('per_total', models.CharField(max_length=30)),
                ('comment', models.CharField(max_length=1000)),
            ],
        ),
    ]
