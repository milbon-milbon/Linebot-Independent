import os
from fastapi import FastAPI
from dotenv import load_dotenv
from app.views import router

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
