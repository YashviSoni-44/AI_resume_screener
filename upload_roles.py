# New file: upload_roles.py
from app.vector_client import init_weaviate, upload_job_roles
client = init_weaviate()
upload_job_roles(client)
