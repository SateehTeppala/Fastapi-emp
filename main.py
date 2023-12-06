from fastapi import FastAPI,Query,Path,Response
from fastapi.responses import JSONResponse

from functools import lru_cache
import pandas as pd
import json

app = FastAPI()

@lru_cache(maxsize=None)
def get_cached_dataframe():
    # Load or compute your DataFrame here
    df1 = pd.read_csv('data/emp.csv')
    return df1

df = get_cached_dataframe()

@app.get('/v1/sample')
def sample_data():
    jd = (df.sample(1)).to_json(orient='records')
    return JSONResponse(json.loads(jd))

@app.get('/v1/sample/{sample_size}')
def sample_data(sample_size: int ):
    jd = (df.sample(sample_size)).to_json(orient='records')
    return JSONResponse(json.loads(jd))


if __name__ == "__main__":
    import uvicorn
    # Run FastAPI using Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
