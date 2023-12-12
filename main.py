from fastapi import FastAPI, Query, Path, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,StreamingResponse
from functools import lru_cache
import pandas as pd
import json
from jai import generate_random_data
from fastapi_redis_cache import FastApiRedisCache, cache
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os


host_url= os.environ['HOST']



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    redis_cache = FastApiRedisCache()
    redis_cache.init(
        host_url= host_url,
        prefix="myapi-cache",
        response_header="X-MyAPI-Cache",
        ignore_arg_types=[Request, Response, Session]
    )
    yield
    # Shutdown logic


app = FastAPI(lifespan=lifespan)
app.add_middleware(GZipMiddleware, minimum_size=10)
templates = Jinja2Templates(directory="templates")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="RaData",  # Replace with your desired API title
        version="2.0",  # Set to an empty string to remove version
        description="IDGAF 🖕",  # Replace with your API description
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@lru_cache(maxsize=None)
def get_cached_dataframe():
    # Load or compute your DataFrame here
    df1 = pd.read_csv('data/emp.csv')
    return df1


df = get_cached_dataframe()


@app.get("/", include_in_schema=False, response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get('/v1/sample')
async def sample_data():
    jd = (df.sample(1)).to_json(orient='records')
    return JSONResponse(json.loads(jd))


@app.get('/v1/sample/{sample_size}')
async def sample_data(sample_size: int = Path(description="Number of samples to retrieve", ge=1, le=1000)):
    jd = (df.sample(sample_size)).to_json(orient='records')
    return JSONResponse(json.loads(jd))


@app.get('/v2/emp/{sample_size}')
@cache(expire=30)
async def fake_data(sample_size: int = Path(description="Number of samples to retrieve", ge=1)):
    # jd = generate_random_data(sample_size)
    # jsd = json.dumps(jd)
    return generate_random_data(sample_size)


if __name__ == "__main__":
    import uvicorn

    # Run FastAPI using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
