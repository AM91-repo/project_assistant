# Generated by Django 3.2.9 on 2022-01-31 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20220131_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseincome',
            name='category',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.category'),
        ),
    ]