from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.views import BookingAdmin, HotelAdmin, RoomAdmin, UserAdmin
from app.bookings.routers import router as booking_router
from app.config import settings
from app.database import engine
from app.hotels.routers import router as hotel_router
from app.users.routers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield

app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine)
admin.add_view(UserAdmin)
admin.add_view(BookingAdmin)
admin.add_view(RoomAdmin)
admin.add_view(HotelAdmin)

app.include_router(booking_router)
app.include_router(user_router)
app.include_router(hotel_router)
