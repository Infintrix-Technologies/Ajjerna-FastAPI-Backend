from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import engine, init_db
# from routers import auth, access, corporate
from apps.auth.views import auth
from apps.users.views import user_route
init_db()
app = FastAPI(
    title="Fast API Auth and User CRUD",
    description="Fast API Project with Authentication and User Crud",

)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth,
                   prefix="/auth",
                   tags=["Authentication"]
                   )
app.include_router(user_route,
                   prefix="/users",
                   tags=["Users"],
                   )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8800)
