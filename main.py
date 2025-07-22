from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import string, random
import sqlalchemy
from contextlib import asynccontextmanager
from database import database, metadata

from database import database, metadata
from models import urls

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

class URLRequest(BaseModel):
    url: HttpUrl

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))

@app.get("/")
async def root():
    return {"message": "URL Shortener API가 정상 작동 중입니다!"}

@app.post("/shorten")
async def shorten_url(request: URLRequest):
    for _ in range(10):
        short_code = generate_short_code()
        query = urls.select().where(urls.c.short_code == short_code)
        existing = await database.fetch_one(query)
        if not existing:
            break
    else:
        raise HTTPException(status_code=500, detail="Failed to generate unique code")

    query = urls.insert().values(short_code=short_code, original_url=str(request.url))
    await database.execute(query)
    return {"short_code": short_code, "short_url": f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
async def redirect_url(short_code: str):
    query = urls.select().where(urls.c.short_code == short_code)
    result = await database.fetch_one(query)
    if result:
        return RedirectResponse(url=result["original_url"])
    raise HTTPException(status_code=404, detail="URL not found")
