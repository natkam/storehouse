# Generated by Django 2.0 on 2017-12-22 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_auto_20171222_0233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transport',
            name='load_type',
            field=models.CharField(choices=[('A', 'Apples'), ('B', 'Bananas'), ('C', 'Carrots'), ('D', 'Dates'), ('E', 'Eggplants')], max_length=15),
        ),
    ]