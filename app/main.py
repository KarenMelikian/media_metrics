from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, submission
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(submission.router, prefix="/api", tags=["Submissions"])
