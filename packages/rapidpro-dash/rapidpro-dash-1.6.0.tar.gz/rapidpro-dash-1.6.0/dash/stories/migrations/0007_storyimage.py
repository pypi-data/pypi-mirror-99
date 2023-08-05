# -*- coding: utf-8 -*-


from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("stories", "0006_auto_20140821_0859")]

    operations = [
        migrations.CreateModel(
            name="StoryImage",
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
                ("name", models.CharField(help_text="The name to describe this image", max_length=64)),
                ("image", models.ImageField(help_text="The image file to use", upload_to="stories")),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=models.PROTECT,
                        help_text="The user which originally created this item",
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
                    "story",
                    models.ForeignKey(
                        help_text="The story to associate to", on_delete=models.PROTECT, to="stories.Story"
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        )
    ]
