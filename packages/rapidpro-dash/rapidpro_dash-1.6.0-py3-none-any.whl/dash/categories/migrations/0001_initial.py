from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("orgs", "0005_orgbackground"), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(help_text="The name of this category", max_length=64)),
                (
                    "image",
                    models.ImageField(
                        help_text="An optional image that can describe this category",
                        null=True,
                        upload_to="categories",
                        blank=True,
                    ),
                ),
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
                        help_text="The organization this category applies to", on_delete=models.PROTECT, to="orgs.Org"
                    ),
                ),
            ],
            options={"verbose_name_plural": "Categories"},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(name="category", unique_together=set([("name", "org")])),
    ]
