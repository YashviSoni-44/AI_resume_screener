# import weaviate
# import os
# from langchain.embeddings import OpenAIEmbeddings

# def init_weaviate():
#     auth_config = weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))
#     client = weaviate.Client(
#         url=os.getenv("WEAVIATE_API_URL"),
#         auth_client_secret=auth_config,
#         additional_headers={"X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY")},
#     )
#     return client

# def upload_job_roles(client, csv_path="data/job_roles.csv"):
#     import pandas as pd
#     df = pd.read_csv(csv_path)
#     for _, row in df.iterrows():
#         job = {
#             "title": row["title"],
#             "description": row["description"]
#         }
#         client.data_object.create(
#             job,
#             "JobRole"
#         )



# import weaviate
# import os
# from dotenv import load_dotenv
# from langchain_community.embeddings import OpenAIEmbeddings

# load_dotenv()  # load .env file

# def init_weaviate():
#     weaviate_url = os.getenv("WEAVIATE_URL")
#     if not weaviate_url:
#         raise ValueError("Missing WEAVIATE_URL in .env file")

#     client = weaviate.Client(url=weaviate_url)
#     return client




import weaviate
import os
from dotenv import load_dotenv
# from langchain_community.embeddings import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings

import pandas as pd


load_dotenv()

def init_weaviate():
    weaviate_url = os.getenv("WEAVIATE_URL")
    username = os.getenv("WEAVIATE_USERNAME")
    password = os.getenv("WEAVIATE_PASSWORD")

    if not (weaviate_url and username and password):
        raise ValueError("Missing WEAVIATE_URL, USERNAME or PASSWORD in .env")

    auth_config = weaviate.AuthClientPassword(
        username=username,
        password=password
    )

    client = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=auth_config
    )
    return client

def upload_job_roles(client, csv_path="data/job_roles.csv"):
    if not client.schema.exists("JobRole"):
        schema = {
            "classes": [
                {
                    "class": "JobRole",
                    "description": "Job roles for resume matching",
                    "vectorizer": "none",  # We will use our own embeddings
                    "properties": [
                        {"name": "title", "dataType": ["text"]},
                        {"name": "description", "dataType": ["text"]},
                    ],
                }
            ]
        }
        client.schema.create(schema)

    df = pd.read_csv(csv_path)
    embedder = OpenAIEmbeddings()

    for _, row in df.iterrows():
        vector = embedder.embed_query(row["description"])
        client.data_object.create(
            data_object={
                "title": row["title"],
                "description": row["description"]
            },
            class_name="JobRole",
            vector=vector
        )
    print("✅ Job roles uploaded to Weaviate")

def match_resume_to_roles(client, resume_text, top_k=1):
    embedder = OpenAIEmbeddings()
    vector = embedder.embed_query(resume_text)

    result = client.query.get("JobRole", ["title", "description"]) \
        .with_near_vector({"vector": vector}) \
        .with_limit(top_k) \
        .do()

    matches = result["data"]["Get"]["JobRole"]
    return matches
