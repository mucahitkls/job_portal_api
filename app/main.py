# app/main.py
from fastapi import FastAPI
from app.routes import user, job, application, auth
from app.dependencies import Base, engine
from app.utils.utilities import get_key
# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Job Search API", version="1.0.0")

# Register Routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(job.router, prefix="/jobs", tags=["jobs"])
app.include_router(application.router, prefix="/applications", tags=["applications"])

API_HOST = get_key('API_HOST')
API_PORT = get_key('API_PORT')
# Add any middleware here

# Include any start-up event handlers

# Include any shutdown event handlers

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_HOST)
