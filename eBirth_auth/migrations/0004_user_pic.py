# Generated by Django 4.1.7 on 2023-03-29 04:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("eBirth_auth", "0003_alter_user_cert_no"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="pic",
            field=models.ImageField(blank=True, null=True, upload_to="uploads/"),
        ),
    ]
