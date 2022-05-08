from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from limiter import RateLimiter
import os

app = FastAPI()

request_num = int(os.environ['REQUEST_NUM'])
duration_seconds = int(os.environ['DURATION_SEC'])

@RateLimiter(request_num, duration_seconds)
def get_response(token):
    # do something
    return {"status_code": 200, "message": "The Task is Successfuly Done!"}


@app.get("/")
async def sample(request: Request):
    try:
        token = request.headers.get('authorization').split(" ")[1]
        response = get_response(token)
        return JSONResponse(status_code=response['status_code'], content=response['message'])
    except:
        raise HTTPException(status_code=403, detail="Permission Denied")
        
