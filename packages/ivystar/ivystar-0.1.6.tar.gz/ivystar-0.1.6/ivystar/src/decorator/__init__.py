#!encoding=utf-8
import time, functools
import multiprocessing
global l
l = multiprocessing.Lock()

'''
装饰器
'''

def timer(func):
    '''
    只打印函数耗时
    '''
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print('excute in {:.2f} 秒'.format(time.time() - start))
        return res
    return wrapper

def prilog(func):
    '''
    打印函数名及耗时
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        start=time.time()
        r=func(*args, **kw)
        print('%s excute in %s ms' %(func.__name__, 1000*(time.time()-start)))
        return r
    return wrapper

def safethread(func):
    '''
    线程安全
    '''
    @functools.wraps(func)
    def wrapper(*args, **kw):
        global l 
        start=time.time()
        l.acquire()
        r=func(*args, **kw)
        print('%s excute in %s ms and lock.acquire()' %(func.__name__, 1000*(time.time()-start)))
        l.release()
        return r
    return wrapper

'''
@log
def fast(x, y):
    return x*y

fast(3, 5)
'''
