from fastapi import FastAPI, UploadFile, Form
from app.vector_client import init_weaviate, match_resume_to_roles
import uvicorn

app = FastAPI()
client = init_weaviate()

@app.post("/analyze")
async def analyze_resume(resume_text: str = Form(...)):
    matches = match_resume_to_roles(client, resume_text)
    return {"matches": matches}

# Optional: For local testing
if __name__ == "__main__":
    uvicorn.run("api.index:app", host="0.0.0.0", port=8000)
