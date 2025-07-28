from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from fastapi import Query
from typing import Optional


app = FastAPI()

# ========== CORS (Allow React frontend to fetch data) ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://www.onlinecoursecompare.com",
        "http://localhost:5173"  # Keep this if you're testing locally too
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# To run the server, use the command:
# .\venv\Scripts\python.exe -m uvicorn main:app --reload

#   When opening a new terminal in PowerShell
# cd backend
# then run: python -m uvicorn main:app --reload 
# ### if not working ####
#  --> .\venv\Scripts\python.exe -m uvicorn main:app --reload

# ========== SQLite DB Setup ==========
DATABASE_URL = "sqlite:///./onlinecoursecompare.db"
engine = create_engine(DATABASE_URL)

# ========== Routes ==========
# @app.get("/")
# def read_root():
#     return {"message": "FastAPI is working!"}

@app.get("/courses")
def get_courses(
    search: Optional[str] = Query(None),
    rating: Optional[float] = Query(None),
    level: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    platform: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(20)
):
    query = "SELECT * FROM courses WHERE 1=1"
    params = {"skip": skip, "limit": limit}

    if search:
        query += " AND LOWER(title) LIKE :search"
        params["search"] = f"%{search.lower()}%"

    if rating:
        query += " AND rating >= :rating"
        params["rating"] = rating

    if level:
        query += " AND LOWER(level) = :level"
        params["level"] = level.lower()

    if max_price is not None:
        query += " AND price <= :max_price"
        params["max_price"] = max_price

    if platform:
        query += " AND LOWER(platform) = :platform"
        params["platform"] = platform.lower().strip()

    query += " LIMIT :limit OFFSET :skip"

    with engine.connect() as conn:
        result = conn.execute(text(query), params)
        courses = result.mappings().all()
    return courses


@app.get("/courses/free")
def get_free_courses(skip: int = Query(0), limit: int = Query(20)):
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM courses WHERE price = 0 LIMIT :limit OFFSET :skip"),
            {"limit": limit, "skip": skip}
        )
        courses = result.mappings().all()
    return courses