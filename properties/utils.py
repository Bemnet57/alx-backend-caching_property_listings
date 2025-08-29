from django.core.cache import cache
from .models import Property

def get_all_properties():
    # Check Redis cache first
    properties = cache.get("all_properties")
    if properties is None:
        # If not cached, query DB
        properties = list(Property.objects.all().values(
            "id", "title", "description", "price", "location", "created_at"
        ))
        # Store in Redis for 1 hour (3600 seconds)
        cache.set("all_properties", properties, 3600)
    return properties
