# ALX Backend Caching — Property Listings
📌 Overview

This project demonstrates caching in Django using PostgreSQL, Redis, and Docker.
It is built around a simple Property Listing application with the following features:

- Dockerized setup with PostgreSQL (database) and Redis (cache).

- Django ORM model for properties.

- View caching with @cache_page.

- Low-level caching using Redis via django-redis.

- Cache invalidation using Django signals.

- Cache metrics analysis to monitor Redis performance.

🛠️ Setup
1. Clone Repository
git clone https://github.com/<your-username>/alx-backend-caching_property_listings.git
cd alx-backend-caching_property_listings

2. Start Services with Docker
docker-compose up -d


This starts:

PostgreSQL → localhost:5432

Redis → localhost:6379

3. Install Dependencies
pip install -r requirements.txt

4. Run Migrations
python manage.py makemigrations
python manage.py migrate

🏗️ Features
1. Property Model

Defined in properties/models.py with fields:

title, description, price, location, created_at.

2. Cached Property List View

Endpoint: http://localhost:8000/properties/

Response cached in Redis for 15 minutes with @cache_page.

3. Low-Level Queryset Caching

Implemented in properties/utils.py:get_all_properties().

Queryset cached in Redis for 1 hour.

4. Cache Invalidation

Signals (post_save, post_delete) delete cache key all_properties.

Implemented in properties/signals.py.

5. Cache Metrics Analysis

properties/utils.py:get_redis_cache_metrics() retrieves:

hits

misses

hit_ratio

Metrics are logged with logger.error.

📊 Example API Response

GET /properties/

{
  "data": [
    {
      "id": 1,
      "title": "Luxury Apartment",
      "description": "Modern 2-bedroom flat",
      "price": "250000.00",
      "location": "Addis Ababa",
      "created_at": "2025-08-28T20:00:00Z"
    }
  ]
}

🚀 Usage
1. Add a Property
python manage.py shell

from properties.models import Property
Property.objects.create(
    title="Luxury Apartment",
    description="Modern 2-bedroom flat",
    price=250000.00,
    location="Addis Ababa"
)

2. Fetch Properties (cached response)
curl http://localhost:8000/properties/


First request → pulls from DB and caches in Redis.

Next requests (within 15 min / 1 hr) → served from Redis instantly.

3. Verify Cache Invalidation

Create or delete another property:

Property.objects.create(title="Villa", description="5-bedroom villa", price=500000.00, location="Nairobi")


→ This will trigger a signal and invalidate the all_properties cache key.

Next call to /properties/ will refresh the cache.

4. Check Cache Metrics

Open Django shell:

python manage.py shell

from properties.utils import get_redis_cache_metrics
print(get_redis_cache_metrics())


Sample output:

{'hits': 12, 'misses': 3, 'hit_ratio': 0.8}

✅ Key Learnings

How to configure Django with PostgreSQL + Redis in Docker.

Different levels of caching in Django (@cache_page vs low-level).

Cache invalidation with signals to avoid stale data.

Using Redis metrics for monitoring cache efficiency.