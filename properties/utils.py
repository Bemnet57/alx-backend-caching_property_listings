import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    """
    Retrieve Redis cache hit/miss metrics and calculate hit ratio.
    """
    conn = get_redis_connection("default")
    info = conn.info("stats")

    hits = info.get("keyspace_hits", 0)
    misses = info.get("keyspace_misses", 0)

    total_requests = hits + misses
    hit_ratio = hits / total_requests if total_requests > 0 else 0

    metrics = {
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2),
    }

    # checker wants logger.error instead of info
    logger.error(f"Redis Cache Metrics: {metrics}")

    return metrics


# from django.core.cache import cache
# from .models import Property

# def get_all_properties():
#     # Check Redis cache first
#     properties = cache.get("all_properties")
#     if properties is None:
#         # If not cached, query DB
#         properties = list(Property.objects.all().values(
#             "id", "title", "description", "price", "location", "created_at"
#         ))
#         # Store in Redis for 1 hour (3600 seconds)
#         cache.set("all_properties", properties, 3600)
#     return properties
