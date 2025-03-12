from fastapi import FastAPI
from routes.generate_route import router

app = FastAPI(
    title="NLP Service",
    description="Handles AI-generated responses using OpenAI.",
    version="1.0.0"
)

# Register routes
app.include_router(router)
