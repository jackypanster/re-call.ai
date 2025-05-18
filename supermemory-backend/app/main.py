from fastapi import FastAPI

app = FastAPI(
    title="SuperMemory API",
    description="Backend service for the re-call (SuperMemory) project.",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "SuperMemory API is running."}
