from fastapi import FastAPI, Query, Path, Response
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.utils import get_openapi
from functools import lru_cache
import pandas as pd
import json

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=1)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Dummy emp details",  # Replace with your desired API title
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

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.get('/v1/sample')
def sample_data():
    jd = (df.sample(1)).to_json(orient='records')
    return JSONResponse(json.loads(jd))


@app.get('/v1/sample/{sample_size}')
def sample_data(sample_size: int):
    jd = (df.sample(sample_size)).to_json(orient='records')
    return JSONResponse(json.loads(jd))


if __name__ == "__main__":
    import uvicorn

    # Run FastAPI using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
