# Generated by Django 2.1.7 on 2019-04-11 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('docview', '0009_auto_20190406_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='Production2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_decl_quantity', models.DecimalField(decimal_places=3, max_digits=7)),
                ('prod_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docview.Batch_pr')),
                ('prod_material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='docview.Raw_material')),
            ],
        ),
        migrations.AlterField(
            model_name='row_id',
            name='r_date',
            field=models.DateField(blank=True, editable=False),
        ),
        migrations.AlterField(
            model_name='row_id',
            name='r_device',
            field=models.CharField(blank=True, editable=False, max_length=3),
        ),
        migrations.AlterField(
            model_name='row_id',
            name='r_time',
            field=models.TimeField(blank=True, editable=False),
        ),
    ]