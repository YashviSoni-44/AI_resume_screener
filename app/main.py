# from fastapi import FastAPI, UploadFile, Form
# from app.resume_agent import analyze_resume
# from app.vector_client import init_weaviate,upload_job_roles
# from tempfile import NamedTemporaryFile

# app = FastAPI()
# client = init_weaviate()

# # def extract_text(file: UploadFile) -> str:
# #     if file.filename.endswith(".pdf"):
# #         import fitz
# #         with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
# #             tmp.write(file.file.read())
# #             doc = fitz.open(tmp.name)
# #             text = "\n".join([page.get_text() for page in doc])
# #             return text
# #     return "Unsupported file"

# @app.post("/analyze/")
# async def analyze(file: UploadFile, job_title: str = Form(...)):
#     resume_text = extract_text(file)

#     # Search Weaviate
#     result = client.query.get("JobRole", ["title", "description"])\
#         .with_near_text({"concepts": [job_title]})\
#         .with_limit(1).do()

#     job_desc = result["data"]["Get"]["JobRole"][0]["description"]
#     analysis = analyze_resume(resume_text, job_desc)
#     return {"analysis": analysis}



from fastapi import FastAPI, UploadFile, Form
from app.vector_client import init_weaviate, match_resume_to_roles
import aiofiles

app = FastAPI()
client = init_weaviate()

@app.post("/analyze")
async def analyze_resume(resume_text: str = Form(...)):
    matches = match_resume_to_roles(client, resume_text)
    return {"matches": matches}
