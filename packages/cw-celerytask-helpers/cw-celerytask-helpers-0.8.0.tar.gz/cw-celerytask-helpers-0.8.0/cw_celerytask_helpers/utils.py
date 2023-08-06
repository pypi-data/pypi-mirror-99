import celery
import redis
from redis.client import Redis


def get_redis_client():
    conf = celery.current_app.conf
    url = conf.get('CUBICWEB_CELERYTASK_REDIS_URL')
    BROKER_TRANSPORT_OPTIONS = conf.get('BROKER_TRANSPORT_OPTIONS')
    if (url and url.startswith('redis-sentinel://')
            and 'sentinels' in BROKER_TRANSPORT_OPTIONS):
        from redis.sentinel import Sentinel
        service_name = BROKER_TRANSPORT_OPTIONS.get('service_name', 'master')
        socket_timeout = BROKER_TRANSPORT_OPTIONS.get('socket_timeout', 3)
        return Sentinel(BROKER_TRANSPORT_OPTIONS['sentinels'],
                        socket_timeout=socket_timeout).master_for(
                            service_name, redis_class=Redis,
                            socket_timeout=socket_timeout)
    elif url:
        return redis.Redis.from_url(url)
