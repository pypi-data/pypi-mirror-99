# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("orgs", "0005_orgbackground")]

    operations = [
        migrations.AlterField(
            model_name="org",
            name="language",
            field=models.CharField(
                choices=[("en", "English"), ("fr", "French")],
                max_length=64,
                blank=True,
                help_text="The main language used by this organization",
                null=True,
                verbose_name="Language",
            ),
        )
    ]
