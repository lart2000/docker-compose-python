# Generated by Django 2.1.5 on 2019-01-15 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
    ]