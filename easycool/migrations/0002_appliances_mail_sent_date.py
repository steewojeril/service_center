# Generated by Django 4.2.2 on 2023-11-28 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easycool', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliances',
            name='mail_sent_date',
            field=models.DateField(default=None, editable=False, null=True),
        ),
    ]