from fastapi import FastAPI
from app.routers.auth import router as auth_router
from app.routers.url_checker import router as url_router
from app.routers.history import router as history_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(url_router)
app.include_router(history_router)

@app.get("/")
def root():
    return {
        "message": "SafeLink API работает"
    }

@app.get("/health")
def health():
    return {
        "status": "OK"
    }
app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)