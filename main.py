from fastapi import FastAPI
from routes import router
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI(title="Koyl AI - Dietary Recommendation API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ping")
def ping():
    return {"message": "Backend is connected!"}
app.include_router(router)
