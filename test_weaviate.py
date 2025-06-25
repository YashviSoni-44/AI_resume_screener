from app.vector_client import init_weaviate

client = init_weaviate()
print("✅ Weaviate Ready:", client.is_ready())
