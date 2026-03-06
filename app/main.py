from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.apis.company_router import router as company_router
from app.apis.user_router import router as user_router
from app.apis.daily_router import router as daily_router
from app.container import create_daily_pipeline, create_user_pipeline
from app.infrastructure.db.session import engine, Base
from app.services.scheduler.daily_scheduler import DailySentimentScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    # When service starts.
    app.state.daily_pipeline = create_daily_pipeline()
    app.state.user_pipeline = create_user_pipeline()
    scheduler = DailySentimentScheduler(pipeline=app.state.daily_pipeline)

    start(scheduler)

    yield

    # When service is stopped.
    shutdown(scheduler)

app = FastAPI(title="Daily News Sentiment API", lifespan=lifespan)

app.include_router(company_router, prefix="/api/company")
app.include_router(user_router, prefix="/api/user")
app.include_router(daily_router, prefix="/api/daily")

def start(scheduler):
    print("Service is started.")

    print("Connecting to DataBase...")
    Base.metadata.create_all(bind=engine)

    print("Scheduler is running...")
    scheduler.start()

def shutdown(scheduler):
    scheduler.shutdown()
    print("Scheduler is stopped...")
    print("Service is stopped.")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
