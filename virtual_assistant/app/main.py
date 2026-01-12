from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.api.routes import router
from app.core.scheduler import scheduler
from app.ml.data_logger import init_logger

# 1️⃣ Create FastAPI app
app = FastAPI(title="Virtual Assistant API")

# 2️⃣ Mount the Static files (The Dashboard)
# This serves files from app/static at the URL /ui
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 3️⃣ Startup events
@app.on_event("startup")
def startup_tasks():
    init_logger()
    print("[FastAPI] Data logger initialized")

@app.on_event("startup")
def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("[FastAPI] Scheduler started")

# 4️⃣ Root route -> Redirect to Dashboard
@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

# 5️⃣ Include routers
app.include_router(router)