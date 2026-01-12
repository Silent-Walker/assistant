from fastapi import FastAPI
from app.api.routes import router
from app.core.scheduler import scheduler
from app.ml.data_logger import init_logger

# 1️⃣ Create FastAPI app FIRST
app = FastAPI(title="Virtual Assistant API")

# 2️⃣ Startup events
@app.on_event("startup")
def startup_tasks():
    init_logger()
    print("[FastAPI] Data logger initialized")

@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("[FastAPI] Scheduler started")

# 3️⃣ Include routers
app.include_router(router)
