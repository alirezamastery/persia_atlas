from django.core.cache import cache

from persia_atlas.cache import CacheKey


def get_online_users() -> set:
    online_users = cache.get(CacheKey.ONLINE_USERS.value)
    if online_users is None:
        return set()
    return online_users


def add_online_user(user_id: int):
    online_users = cache.get(CacheKey.ONLINE_USERS.value)
    if online_users is None:
        cache.set(CacheKey.ONLINE_USERS.value, {user_id})
    else:
        online_users.add(user_id)
        cache.set(CacheKey.ONLINE_USERS.value, online_users)


def remove_online_user(user_id: int):
    online_users = cache.get(CacheKey.ONLINE_USERS.value)
    if online_users is None:
        cache.set(CacheKey.ONLINE_USERS.value, set())
    else:
        online_users.discard(user_id)
        cache.set(CacheKey.ONLINE_USERS.value, online_users)


def get_user_status(user_id: int):
    online_users = get_online_users()
    return user_id in online_users


__all__ = [
    'get_online_users',
    'add_online_user',
    'remove_online_user',
    'get_user_status',
]
