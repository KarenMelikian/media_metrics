from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from routers import auth, user_inputs, user, export_import_csv


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def serve_index():
    return FileResponse("frontend/index.html")

@app.get("/dashboard")
def serve_dashboard():
    return FileResponse("frontend/dashboard.html")



app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(user.router, prefix="/api/user", tags=["User"])
app.include_router(user_inputs.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(export_import_csv.router, prefix="/api/csv", tags=["CSV"])



if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, host='0.0.0.0', port=8000)
