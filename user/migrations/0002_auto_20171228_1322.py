# Generated by Django 2.0 on 2017-12-28 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutor',
            name='salary',
            field=models.FloatField(blank=True, max_length=5, null=True),
        ),
    ]
