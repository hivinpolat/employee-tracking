# Generated by Django 5.1.3 on 2024-11-29 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("tracking", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="leaverequest",
            name="approved",
            field=models.BooleanField(default=False),
        ),
    ]
