# Generated by Django 2.1.5 on 2019-01-17 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('countries', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='code',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='country',
            name='currency',
            field=models.CharField(max_length=3),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
