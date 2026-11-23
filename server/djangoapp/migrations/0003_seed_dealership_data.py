import json
from datetime import datetime
from pathlib import Path

from django.db import migrations


def seed_dealership_data(apps, schema_editor):
    Dealership = apps.get_model("djangoapp", "Dealership")
    Review = apps.get_model("djangoapp", "Review")
    ContactMessage = apps.get_model("djangoapp", "ContactMessage")

    # The first Render deployment recorded an older 0001 migration which only
    # contained the vehicle catalog. Create the newer tables when upgrading
    # that database; fresh installations already have them and skip this step.
    existing_tables = set(schema_editor.connection.introspection.table_names())
    for model in (Dealership, Review, ContactMessage):
        if model._meta.db_table not in existing_tables:
            schema_editor.create_model(model)
            existing_tables.add(model._meta.db_table)

    data_dir = Path(__file__).resolve().parents[2] / "database" / "data"

    dealerships = json.loads(
        (data_dir / "dealerships.json").read_text(encoding="utf-8")
    )["dealerships"]
    reviews = json.loads(
        (data_dir / "reviews.json").read_text(encoding="utf-8")
    )["reviews"]

    for item in dealerships:
        Dealership.objects.update_or_create(id=item["id"], defaults=item)

    for item in reviews:
        defaults = {**item}
        defaults.pop("id", None)
        defaults["dealership_id"] = defaults.pop("dealership")
        date_value = defaults.get("purchase_date")
        defaults["purchase_date"] = (
            datetime.strptime(date_value, "%m/%d/%Y").date()
            if date_value else None
        )
        defaults["sentiment"] = "neutral"
        Review.objects.update_or_create(id=item["id"], defaults=defaults)


class Migration(migrations.Migration):
    dependencies = [("djangoapp", "0002_seed_cars")]
    operations = [
        migrations.RunPython(seed_dealership_data, migrations.RunPython.noop),
    ]
