from django.contrib import admin

from .models import CarMake, CarModel, ContactMessage, Dealership, Review


class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 0


@admin.register(CarMake)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = (CarModelInline,)


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ("name", "car_make", "type", "year")
    list_filter = ("car_make", "type", "year")


@admin.register(Dealership)
class DealershipAdmin(admin.ModelAdmin):
    list_display = ("full_name", "city", "state", "zip")
    list_filter = ("state",)
    search_fields = ("full_name", "city", "address")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("name", "dealership", "car_make", "car_model", "sentiment")
    list_filter = ("sentiment", "car_make")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "message")
