# Generated by Django 2.0 on 2017-12-19 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20171219_0043'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transport',
            options={'ordering': ['number']},
        ),
    ]
