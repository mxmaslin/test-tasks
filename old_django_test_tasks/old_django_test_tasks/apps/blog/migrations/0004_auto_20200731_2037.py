# Generated by Django 2.1.1 on 2020-07-31 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200731_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to='blog/images/%Y/%m/%d'),
        ),
    ]
