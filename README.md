# ALX Travel App — 0x00

Implements models, serializers, and a seeding command for the `listings` app.

## Commands
```bash
python manage.py makemigrations listings
python manage.py migrate
python manage.py seed --purge --listings 15
Files
alx_travel_app/listings/models.py

alx_travel_app/listings/serializers.py