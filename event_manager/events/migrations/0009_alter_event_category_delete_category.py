# Generated by Django 4.2.10 on 2024-04-17 06:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("categories", "0001_initial"),
        ("events", "0008_category_event_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="events",
                to="categories.category",
                verbose_name="категория",
            ),
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]