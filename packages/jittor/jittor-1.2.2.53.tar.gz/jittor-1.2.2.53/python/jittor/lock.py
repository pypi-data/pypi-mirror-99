import fcntl
import os
from jittor_utils import cache_path, LOG

class Lock:   
    def __init__(self, filename):  
        self.handle = open(filename, 'w')
        LOG.v(f'OPEN LOCK path: {filename} PID: {os.getpid()}')
        self.is_locked = False
      
    def lock(self):  
        fcntl.flock(self.handle, fcntl.LOCK_EX)
        self.is_locked = True
        LOG.vv(f'LOCK PID: {os.getpid()}')
        
    def unlock(self):  
        fcntl.flock(self.handle, fcntl.LOCK_UN)
        self.is_locked = False
        LOG.vv(f'UNLOCK PID: {os.getpid()}')
        
    def __del__(self):  
        self.handle.close()


class _base_scope:
    '''base_scope for support @xxx syntax'''
    def __enter__(self): pass
    def __exit__(self, *exc): pass
    def __call__(self, func):
        def inner(*args, **kw):
            with self:
                ret = func(*args, **kw)
            return ret
        return inner

class lock_scope(_base_scope):
    def __enter__(self):
        self.is_locked = jittor_lock.is_locked
        if not self.is_locked:
            jittor_lock.lock()

    def __exit__(self, *exc):
        if not self.is_locked:
            jittor_lock.unlock()

class unlock_scope(_base_scope):
    def __enter__(self):
        self.is_locked = jittor_lock.is_locked
        if self.is_locked:
            jittor_lock.unlock()

    def __exit__(self, *exc):
        if self.is_locked:
            jittor_lock.lock()

lock_path = os.path.abspath(os.path.join(cache_path, "../jittor.lock"))
if not os.path.exists(lock_path):
    LOG.i("Create lock file:", lock_path)
    try:
        os.mknod(lock_path)
    except:
        pass
jittor_lock = Lock(lock_path)
