# -*- coding: utf-8 -*-


from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("orgs", "0004_auto_20140804_1453")]

    operations = [
        migrations.CreateModel(
            name="OrgBackground",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                (
                    "is_active",
                    models.BooleanField(
                        default=True, help_text="Whether this item is active, use this instead of deleting"
                    ),
                ),
                (
                    "created_on",
                    models.DateTimeField(help_text="When this item was originally created", auto_now_add=True),
                ),
                ("modified_on", models.DateTimeField(help_text="When this item was last modified", auto_now=True)),
                (
                    "name",
                    models.CharField(
                        help_text="The name to describe this background", max_length=128, verbose_name="Name"
                    ),
                ),
                (
                    "background_type",
                    models.CharField(
                        default="P",
                        max_length=1,
                        verbose_name="Background type",
                        choices=[("B", "Banner"), ("P", "Pattern")],
                    ),
                ),
                ("image", models.ImageField(help_text="The image file", upload_to="org_bgs")),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user which originally created this item",
                        on_delete=models.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "modified_by",
                    models.ForeignKey(
                        help_text="The user which last modified this item",
                        on_delete=models.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "org",
                    models.ForeignKey(
                        verbose_name="Org",
                        on_delete=models.PROTECT,
                        to="orgs.Org",
                        help_text="The organization in which the image will be used",
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        )
    ]
