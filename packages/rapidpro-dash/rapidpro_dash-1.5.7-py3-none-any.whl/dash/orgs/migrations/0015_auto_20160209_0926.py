# -*- coding: utf-8 -*-


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("orgs", "0014_auto_20150722_1419")]

    operations = [
        migrations.CreateModel(
            name="TaskState",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("task_key", models.CharField(max_length=32)),
                ("started_on", models.DateTimeField(null=True)),
                ("ended_on", models.DateTimeField(null=True)),
                ("last_successfully_started_on", models.DateTimeField(null=True)),
                ("last_results", models.TextField(null=True)),
                ("is_failing", models.BooleanField(default=False)),
                ("org", models.ForeignKey(related_name="task_states", on_delete=models.PROTECT, to="orgs.Org")),
            ],
        ),
        migrations.AlterUniqueTogether(name="taskstate", unique_together=set([("org", "task_key")])),
    ]
