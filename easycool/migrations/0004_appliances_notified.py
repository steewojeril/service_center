# Generated by Django 4.2.2 on 2023-11-28 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('easycool', '0003_remove_appliances_mail_sent_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appliances',
            name='notified',
            field=models.BooleanField(default=False, editable=False, null=True),
        ),
    ]
