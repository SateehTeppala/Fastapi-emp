from fastapi import FastAPI, Query, Path, Response, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,StreamingResponse
from functools import lru_cache
import pandas as pd
import json
from jai import generate_random_data,v3_generate_random_data

import random


import ssl

app = FastAPI()

# Startup logic
# async def startup_event():
#     redis_cache = FastApiRedisCache()
#     redis_cache.init(
#         host_url=host_url,
#         prefix="myapi-cache",
#         response_header="X-MyAPI-Cache",
#         ignore_arg_types=[Request, Response],
#     )

# Shutdown logic
# async def shutdown_event():
#     pass  # You can add shutdown logic here

# Register startup and shutdown events
# app.add_event_handler("startup", startup_event)
# app.add_event_handler("shutdown", shutdown_event)
app.add_middleware(GZipMiddleware, minimum_size=1)
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
    return "Hello,world"
    # return templates.TemplateResponse('index.html', {"request": request})


@app.get('/v1/sample')
async def sample_data():
    jd = (df.sample(1)).to_json(orient='records')
    return JSONResponse(json.loads(jd))


@app.get('/v1/sample/{sample_size}')
async def sample_data(sample_size: int = Path(description="Number of samples to retrieve", ge=1, le=10)):
    jd = (df.sample(sample_size)).to_json(orient='records')
    response = JSONResponse(json.loads(jd))
    response.headers["Cache-Control"] = "max-age=300, must-revalidate"

    return response

@app.get('/v1/emp/{emp_id}')
async def get_employee(emp_id: int = Path(description="Employee ID")):
    # Find the employee data based on the provided id
    employee_data = df[df['id'] == emp_id].to_dict(orient='records')
    if not employee_data:
        return JSONResponse(content={"error": "Employee not found"}, status_code=404)
    response = JSONResponse(content=employee_data[0])
    response.headers["Cache-Control"] = "max-age=300, must-revalidate"

    return response

@app.get('/v2/emp/{sample_size}')
# @cache(expire=30)
async def fake_data(sample_size: int = Path(description="Number of samples to retrieve", ge=1,le=10)):
    # jd = generate_random_data(sample_size)
    # jsd = json.dumps(jd)
    return generate_random_data(sample_size)

@app.get('/v2/emp/getdata/')
async def fake_data():
    return v3_generate_random_data()

@app.get('/random/data/')
async def random_data():
    random_number = random.randint(1000, 10000)
    return generate_random_data(random_number)

@app.get('/data')
async def random_data():
    return generate_random_data(10000)

if __name__ == "__main__":
    import uvicorn

    # Run FastAPI using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
