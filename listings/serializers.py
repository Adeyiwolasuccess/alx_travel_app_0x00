from rest_framework import serializers
from ...alx_travel_app.listings.models import Listing, Booking


class ListingSerializer(serializers.ModelSerializer):
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True, required=False)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Listing
        fields = [
            "id", "title", "description", "city", "country",
            "price_per_night", "max_guests", "is_active",
            "average_rating", "reviews_count", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at", "average_rating", "reviews_count"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["average_rating"] = instance.average_rating if instance.average_rating is not None else None
        data["reviews_count"] = getattr(instance, "reviews__count", None) or instance.reviews.count()
        return data


class BookingSerializer(serializers.ModelSerializer):
    listing_title = serializers.CharField(source="listing.title", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id", "listing", "listing_title", "guest_name", "guests",
            "start_date", "end_date", "status", "total_price",
            "created_at", "updated_at",
        ]
        read_only_fields = ["status", "total_price", "created_at", "updated_at"]
