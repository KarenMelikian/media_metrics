from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers import auth, submission, user


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(submission.router, prefix="/api/submissions", tags=["Submissions"])



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8000)
