from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.endpoints import login, profile, register, forgot_password, reset_password, confirm_email
from .db.init_db import init_db

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(register.router, prefix="/users", tags=["register"])
app.include_router(confirm_email.router, prefix="/users", tags=["confirm_email"])
app.include_router(login.router, prefix="/users", tags=["auth"])
app.include_router(forgot_password.router, prefix="/users", tags=["forget_password"])
app.include_router(reset_password.router, prefix="/users", tags=["reset_password"])
app.include_router(profile.router, prefix="/users", tags=["profile"])
