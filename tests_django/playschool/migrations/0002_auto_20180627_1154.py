# Generated by Django 2.0.4 on 2018-06-27 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playschool', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scholar',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='playschool/images/%Y/%m/%d'),
        ),
    ]