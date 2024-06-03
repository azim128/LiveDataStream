from config import logging_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.router import router

app = FastAPI()

# Configure logging
logging_config.setup_logging()

allowed_origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


# health check
@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
