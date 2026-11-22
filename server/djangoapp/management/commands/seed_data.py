import json
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from djangoapp.models import CarMake, CarModel, Dealership, Review


class Command(BaseCommand):
    help = "Seed the local database from the supplied capstone JSON datasets."

    def handle(self, *args, **options):
        data_dir = Path(settings.BASE_DIR) / "database" / "data"
        dealerships = json.loads(
            (data_dir / "dealerships.json").read_text(encoding="utf-8")
        )["dealerships"]
        reviews = json.loads(
            (data_dir / "reviews.json").read_text(encoding="utf-8")
        )["reviews"]
        cars = json.loads(
            (data_dir / "car_records.json").read_text(encoding="utf-8")
        )["cars"]

        for item in dealerships:
            Dealership.objects.update_or_create(id=item["id"], defaults=item)

        for item in cars:
            make, _ = CarMake.objects.get_or_create(
                name=item["make"], defaults={"description": f"{item['make']} vehicles"}
            )
            CarModel.objects.update_or_create(
                car_make=make, name=item["model"],
                defaults={"type": item.get("bodyType") or "Other", "year": item["year"]},
            )

        for item in reviews:
            date_value = item.get("purchase_date")
            purchase_date = datetime.strptime(date_value, "%m/%d/%Y").date() if date_value else None
            text = item["review"]
            lowered = text.lower()
            positive = any(word in lowered for word in ("great", "good", "excellent", "friendly", "helpful"))
            negative = any(word in lowered for word in ("bad", "poor", "rude", "terrible", "worst"))
            sentiment = "positive" if positive and not negative else "negative" if negative else "neutral"
            defaults = {**item, "purchase_date": purchase_date, "sentiment": sentiment}
            defaults.pop("id", None)
            defaults["dealership_id"] = defaults.pop("dealership")
            Review.objects.update_or_create(id=item["id"], defaults=defaults)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Dealership.objects.count()} dealers, "
            f"{Review.objects.count()} reviews, and {CarModel.objects.count()} car models."
        ))
