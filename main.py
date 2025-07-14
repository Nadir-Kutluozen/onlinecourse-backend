from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

app = FastAPI()

# ========== CORS (Allow React frontend to fetch data) ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Your React dev server
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
def get_courses():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM courses"))
        print(result.keys)
        courses = result.mappings().all()
    return courses