from django.db import migrations


def seed_cars(apps, schema_editor):
    CarMake = apps.get_model('djangoapp', 'CarMake')
    CarModel = apps.get_model('djangoapp', 'CarModel')
    cars = [('Nissan', 'Pathfinder', 'SUV', 2023), ('Kia', 'Seltos', 'SUV', 2022),
            ('Audi', 'A4', 'Sedan', 2021), ('Mercedes', 'GLE', 'SUV', 2020),
            ('Toyota', 'Camry', 'Sedan', 2023), ('Honda', 'CR-V', 'SUV', 2022)]
    for make_name, model_name, body_type, year in cars:
        make, _ = CarMake.objects.get_or_create(name=make_name)
        CarModel.objects.get_or_create(car_make=make, name=model_name, type=body_type, year=year)


class Migration(migrations.Migration):
    dependencies = [('djangoapp', '0001_initial')]
    operations = [migrations.RunPython(seed_cars, migrations.RunPython.noop)]
