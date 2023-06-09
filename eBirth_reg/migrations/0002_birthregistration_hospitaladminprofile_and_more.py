# Generated by Django 4.1.7 on 2023-03-26 18:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("eBirth_reg", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BirthRegistration",
            fields=[
                (
                    "birth_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("child_name", models.CharField(max_length=100)),
                ("father_name", models.CharField(max_length=100)),
                ("mother_name", models.CharField(max_length=100)),
                ("date_time", models.DateTimeField()),
                ("weight", models.CharField(max_length=10)),
                ("delivered_by", models.CharField(max_length=100)),
                ("certificate_num", models.CharField(max_length=10)),
                ("date_issue", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="HospitalAdminProfile",
            fields=[
                (
                    "admin_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(name="CitizenProfile",),
        migrations.AddField(
            model_name="hospitalprofile",
            name="hospital_address",
            field=models.CharField(default="", max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hospitalprofile",
            name="hospital_name",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="hospitaladminprofile",
            name="hospital_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="eBirth_reg.hospitalprofile",
            ),
        ),
        migrations.AddField(
            model_name="hospitaladminprofile",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="birthregistration",
            name="place_of_birth",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="eBirth_reg.hospitalprofile",
            ),
        ),
        migrations.AddField(
            model_name="birthregistration",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
