## Scalability Notes

### Current Architecture
- Django REST Framework + SQLite (dev) / PostgreSQL (prod)
- JWT stateless auth → no session store needed

### Horizontal Scaling (Load Balancing)
- Stateless JWT means any backend instance handles any request.
- Deploy behind Nginx → Gunicorn (multiple workers) or use AWS ALB.
- Use `gunicorn --workers 4 backend.wsgi` for multi-process serving.

### Database Scaling
- Move from SQLite to PostgreSQL with read replicas for heavy reads.
- Add indexes on `tasks.owner` and `tasks.status` (already via ForeignKey).
- Use Django's `select_related` / `prefetch_related` to avoid N+1 queries.

### Caching (Redis)
- Cache user profile (`/auth/me/`) in Redis with a 5-min TTL.
- Use `django-redis` as the cache backend.
- Cache task list responses for admin users (invalidate on write).

### Microservices Path
- Split `accounts` and `tasks` into separate services with shared JWT secret.
- API Gateway (e.g., Kong or AWS API Gateway) routes and rate-limits.
- Message queue (Celery + Redis) for async tasks like email notifications.

### Docker Deployment
- Dockerfile + docker-compose.yml with: django, postgres, redis, nginx services.
- Use environment variables (`.env`) for all secrets — never hardcode.