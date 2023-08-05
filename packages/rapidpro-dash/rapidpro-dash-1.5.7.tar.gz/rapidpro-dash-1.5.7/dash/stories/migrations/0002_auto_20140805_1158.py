# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("stories", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="story",
            name="image",
            field=models.ImageField(
                help_text="Any image that should be displayed with this story",
                null=True,
                upload_to="stories",
                blank=True,
            ),
        )
    ]
