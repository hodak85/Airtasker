#!/bin/bash
import redis as rds
import time


def RateLimiter(limited_number, time_window):
    conn = rds.Redis(host='redis', port=6379, decode_responses=True, db=0)
    p = conn.pipeline()
    def decorator(func):
        def rateLimiterFunction(*args, **kargs):
            _requests = conn.keys(f"{args[0]}-*")
            _min_time = min(_requests).split("-")[1] if len(_requests) > 0 else 0 
            while len(_requests) > 0:
                p.get(_requests.pop())
            result = p.execute()
            _total_req = [int(x) for x in result]
            if sum(_total_req) >= limited_number:
                diff_time = int(time.time()) - int(_min_time)
                response = {"status_code": 429, "message": f"Rate limit exceeded. Try again in {time_window - diff_time} seconds"}
                
            else:
                now = str(int(time.time()))
                _key = f"{args[0]}-{now}"
                p.incr(_key)
                p.expire(_key, time_window)
                p.execute()
                response = func(*args, **kargs)
            return response
        return rateLimiterFunction
    return decorator

