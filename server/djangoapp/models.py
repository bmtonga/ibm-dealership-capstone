from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class CarMake(models.Model):
    name = models.CharField(max_length=80, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    TYPES = [(value, value) for value in (
        "Sedan", "SUV", "Hatchback", "Coupe", "Convertible", "Pickup",
        "Minivan", "Wagon", "Other",
    )]
    car_make = models.ForeignKey(
        CarMake, on_delete=models.CASCADE, related_name="models"
    )
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=30, choices=TYPES, default="Other")
    year = models.IntegerField(
        validators=[MinValueValidator(1990), MaxValueValidator(2035)]
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=("car_make", "name"), name="unique_car_model"
        )]
        ordering = ("car_make__name", "name")

    def __str__(self):
        return f"{self.car_make.name} {self.name}"


class Dealership(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, db_index=True)
    st = models.CharField(max_length=3)
    address = models.CharField(max_length=180)
    zip = models.CharField(max_length=12)
    lat = models.FloatField(null=True, blank=True)
    long = models.FloatField(null=True, blank=True)
    short_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=180)

    class Meta:
        ordering = ("full_name", "id")

    def __str__(self):
        return self.full_name

    def as_dict(self):
        return {
            "id": self.id, "city": self.city, "state": self.state,
            "st": self.st, "address": self.address, "zip": self.zip,
            "lat": self.lat, "long": self.long,
            "short_name": self.short_name, "full_name": self.full_name,
        }


class Review(models.Model):
    name = models.CharField(max_length=140)
    dealership = models.ForeignKey(
        Dealership, on_delete=models.CASCADE, related_name="reviews"
    )
    review = models.TextField()
    purchase = models.BooleanField(default=True)
    purchase_date = models.DateField(null=True, blank=True)
    car_make = models.CharField(max_length=80)
    car_model = models.CharField(max_length=100)
    car_year = models.PositiveIntegerField()
    sentiment = models.CharField(max_length=12, default="neutral")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def as_dict(self):
        return {
            "id": self.id, "name": self.name,
            "dealership": self.dealership_id, "review": self.review,
            "purchase": self.purchase,
            "purchase_date": self.purchase_date.isoformat()
            if self.purchase_date else None,
            "car_make": self.car_make, "car_model": self.car_model,
            "car_year": self.car_year, "sentiment": self.sentiment,
        }


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
