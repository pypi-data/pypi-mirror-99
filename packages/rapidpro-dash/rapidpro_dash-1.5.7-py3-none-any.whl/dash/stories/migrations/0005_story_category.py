# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("categories", "0002_auto_20140820_1415"), ("stories", "0004_auto_20140806_1540")]

    operations = [
        migrations.AddField(
            model_name="story",
            name="category",
            field=models.ForeignKey(
                blank=True,
                to="categories.Category",
                on_delete=models.PROTECT,
                help_text="The category for this story",
                null=True,
            ),
            preserve_default=True,
        )
    ]
