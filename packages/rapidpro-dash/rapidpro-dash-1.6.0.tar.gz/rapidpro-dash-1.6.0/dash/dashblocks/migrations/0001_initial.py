from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("orgs", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="DashBlock",
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
                    "title",
                    models.CharField(
                        help_text="The title for this block of content, optional",
                        max_length=255,
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "summary",
                    models.TextField(help_text="The summary for this item, should be short", null=True, blank=True),
                ),
                (
                    "content",
                    models.TextField(
                        help_text="The body of text for this content block, optional", null=True, blank=True
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        help_text="Any image that should be displayed with this content block, optional",
                        null=True,
                        upload_to="dashblocks",
                        blank=True,
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        help_text="A background color to use for the image, in the format: #rrggbb",
                        max_length=16,
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "link",
                    models.CharField(
                        help_text="Any link that should be associated with this content block, optional",
                        max_length=255,
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "video_id",
                    models.CharField(
                        help_text="The id of the YouTube video that should be linked to this item",
                        max_length=255,
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "tags",
                    models.CharField(
                        help_text="Any tags for this content block, separated by spaces, can be used to do more advanced filtering, optional",
                        max_length=255,
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        default=0, help_text="The priority for this block, higher priority blocks come first"
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
                        help_text="The organization this content block belongs to",
                        on_delete=models.PROTECT,
                        to="orgs.Org",
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="DashBlockImage",
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
                    "image",
                    models.ImageField(height_field="height", width_field="width", upload_to="dashblock_images/"),
                ),
                ("caption", models.CharField(max_length=64)),
                ("priority", models.IntegerField(default=0, null=True, blank=True)),
                ("width", models.IntegerField()),
                ("height", models.IntegerField()),
                (
                    "created_by",
                    models.ForeignKey(
                        help_text="The user which originally created this item",
                        on_delete=models.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("dashblock", models.ForeignKey(to="dashblocks.DashBlock", on_delete=models.PROTECT)),
                (
                    "modified_by",
                    models.ForeignKey(
                        help_text="The user which last modified this item",
                        on_delete=models.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="DashBlockType",
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
                        help_text="The human readable name for this content type", unique=True, max_length=75
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="The slug to idenfity this content type, used with the template tags", unique=True
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        help_text="A description of where this content type is used on the site and how it will be dsiplayed",
                        null=True,
                        blank=True,
                    ),
                ),
                (
                    "has_title",
                    models.BooleanField(default=True, help_text="Whether this content should include a title"),
                ),
                (
                    "has_image",
                    models.BooleanField(default=True, help_text="Whether this content should include an image"),
                ),
                (
                    "has_rich_text",
                    models.BooleanField(default=True, help_text="Whether this content should use a rich HTML editor"),
                ),
                (
                    "has_summary",
                    models.BooleanField(default=True, help_text="Whether this content should include a summary field"),
                ),
                (
                    "has_link",
                    models.BooleanField(default=True, help_text="Whether this content should include a link"),
                ),
                (
                    "has_gallery",
                    models.BooleanField(
                        default=False,
                        help_text="Whether this content should allow upload of additional images, ie a gallery",
                    ),
                ),
                ("has_color", models.BooleanField(default=False, help_text="Whether this content has a color field")),
                (
                    "has_video",
                    models.BooleanField(
                        default=False, help_text="Whether this content should allow setting a YouTube id"
                    ),
                ),
                ("has_tags", models.BooleanField(default=False, help_text="Whether this content should allow tags")),
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
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name="dashblock",
            name="dashblock_type",
            field=models.ForeignKey(
                verbose_name="Content Type",
                on_delete=models.PROTECT,
                to="dashblocks.DashBlockType",
                help_text="The category, or type for this content block",
            ),
            preserve_default=True,
        ),
    ]
