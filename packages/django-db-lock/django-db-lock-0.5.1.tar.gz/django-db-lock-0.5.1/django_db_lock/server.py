
import time
import logging
import datetime

from django.urls import path
from django.utils import timezone
from django.db.utils import IntegrityError
from django.db import transaction

try:
    from django_redis import get_redis_connection
except ImportError:
    get_redis_connection = None

from django_apiview.views import apiview

from . import settings

logger = logging.getLogger(__name__)

class DjangoDbLockServer(object):

    def __init__(self, model, use_redis_cache=None, redis_cache_name=None, redis_cache_prefix=None):
        self.model = model
        self.use_redis_cache = use_redis_cache or settings.DJANGO_DB_LOCK_USA_REDIS_CACHE
        self.redis_cache_name = redis_cache_name or settings.DJANGO_DB_LOCK_REDIS_CACHE_NAME
        self.redis_cache_prefix = redis_cache_prefix or settings.DJANGO_DB_LOCK_REDIS_CACHE_PREFIX
        self.redis_cache_enabled = self.get_redis_cache_enabled()

    def get_redis_cache_enabled(self):
        if not self.use_redis_cache:
            return False
        if not get_redis_connection:
            return False
        try:
            db = get_redis_connection(self.redis_cache_name)
            return db.ping()
        except Exception:
            return False

    def get_redis_connection(self):
        if self.enable_redis_cache:
            return get_redis_connection(self.redis_cache_name)
        else:
            return None

    def get_redis_lock_cache_key(self, lock_name):
        return ":".join([self.redis_cache_prefix, lock_name])
    
    def clear_expired_locks(self):
        try:
            return self._clear_expired_locks()
        except Exception as error:
            logger.exception("clear_expired_locks failed: error_message={}".format(error))

    def _clear_expired_locks(self):
        now_time = timezone.now()
        with transaction.atomic():
            self.model.objects.filter(expire_time__lte=now_time).delete()


    def acquire_lock(self, lock_name, worker_name, timeout):
        self.clear_expired_locks()
        expire_at = int(time.time() + timeout)
        result1 = self.acquire_lock_in_redis(lock_name, worker_name, expire_at)
        if not result1:
            return result1
        result2 = self.acquire_lock_in_database(lock_name, worker_name, expire_at)
        return result2

    def acquire_lock_in_redis(self, lock_name, worker_name, expire_at):
        try:
            return self._acquire_lock_in_redis(lock_name, worker_name, expire_at)
        except Exception as error:
            logger.exception("acquire_lock_in_redis failed, lock_name={} worker_name={} expire_at={} error_message={0}".format(lock_name, worker_name, expire_at, error))
            return False

    def _acquire_lock_in_redis(self, lock_name, worker_name, expire_at):
        if not self.redis_cache_enabled:
            return True
        db = self.get_redis_connection()
        key = self.get_redis_lock_cache_key(lock_name)
        flag = db.setnx(key, worker_name)
        if flag:
            db.expireat(key, expire_at)
        return flag

    def acquire_lock_in_database(self, lock_name, worker_name, expire_at):
        try:
            return self._acquire_lock_in_database(lock_name, worker_name, expire_at)
        except Exception as error:
            logger.exception("acquire_lock_in_database failed, lock_name={} worker_name={} error_message={0}".format(lock_name, worker_name, error))
            return False

    def _acquire_lock_in_database(self, lock_name, worker_name, expire_at): 
        lock = self.model()
        lock.lock_name = lock_name
        lock.worker_name = worker_name
        lock.lock_time = timezone.now()
        lock.expire_time = timezone.make_aware(datetime.datetime.fromtimestamp(expire_at))
        try:
            with transaction.atomic():
                lock.save()
            return True
        except IntegrityError:
            return False

    def release_lock(self, lock_name, worker_name):
        self.clear_expired_locks()
        result1 = self.release_lock_in_database(lock_name, worker_name)
        result2 = self.release_lock_in_redis(lock_name, worker_name)
        return result1 and result2

    def release_lock_in_redis(self, lock_name, worker_name):
        try:
            return self._release_lock_in_redis(lock_name, worker_name)
        except Exception:
            logger.exception("release_lock_in_redis failed: lock_name={} worker_name={} error_message={}".format(lock_name, worker_name, error))
            return False

    def _release_lock_in_redis(self, lock_name, worker_name):
        if self.redis_cache_enabled:
            db = self.get_redis_connection()
            key = self.get_redis_lock_cache_key(lock_name)
            real_worker_name = db.get(key)
            if real_worker_name == worker_name:
                db.delete(key)
        return True

    def release_lock_in_database(self, lock_name, worker_name):
        try:
            return self._release_lock_in_database(lock_name, worker_name)
        except Exception as error:
            logger.exception("release_lock_in_database failed: lock_name={} worker_name={} error_message={}".format(lock_name, worker_name, error))
            return False

    def _release_lock_in_database(self, lock_name, worker_name):
        try:
            lock = self.model.objects.get(lock_name=lock_name, worker_name=worker_name)
            with transaction.atomic():
                lock.delete()
        except self.model.DoesNotExist:
            pass
        return True

    def get_lock_info(self, lock_name):
        try:
            lock = self.model.objects.get(lock_name=lock_name)
            return {
                "pk": lock.pk,
                "lockName": lock.lock_name,
                "workerName": lock.worker_name,
                "lockTime": lock.lock_time,
                "expireTime": lock.expire_time,
            }
        except self.model.DoesNotExist:
            return None

    def get_urls(self, prefix="django_db_lock"):
        return [
            path('acquireLock', self.getAcquireLockView(), name=prefix + ".acquireLock"),
            path('releaseLock', self.getReleaseLockView(), name=prefix + ".releaseLock"),
            path('getLockInfo', self.getGetLockInfoView(), name=prefix + ".getLockInfo"),
            path('clearExpiredLocks', self.GetClearExpiredLocksView(), name=prefix + ".clearExpiredLocks"),
        ]

    def getAcquireLockView(self):
        @apiview
        def acquireLock(lockName, workerName, timeout:int):
            result = self.acquire_lock(lockName, workerName, timeout)
            return result
        return acquireLock

    def getReleaseLockView(self):
        @apiview
        def releaseLock(lockName, workerName):
            result = self.release_lock(lockName, workerName)
            return result
        return releaseLock

    def getGetLockInfoView(self):
        @apiview
        def getLockInfo(lockName):
            info = self.get_lock_info(lockName)
            return info
        return getLockInfo

    def GetClearExpiredLocksView(self):
        @apiview
        def clearExpiredLocks():
            self.clear_expired_locks()
            return True
        return clearExpiredLocks

if settings.DJANGO_DB_LOCK_AUTO_REGISTER_SERVICES and settings.DJANGO_DB_LOCK_AUTO_REGISTER_MODEL:
    from .models import Lock
    django_db_lock_default_server = DjangoDbLockServer(Lock)
