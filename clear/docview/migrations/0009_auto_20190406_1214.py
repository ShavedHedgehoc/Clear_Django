# Generated by Django 2.1.7 on 2019-04-06 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docview', '0008_auto_20190406_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='raw_material',
            name='barcode',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
    ]