#!encoding=utf-8
import time, functools

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

def log(func):
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

'''
@log
def fast(x, y):
    return x*y

fast(3, 5)
'''
