import chromadb
from settings import vector_db_path
from chromadb.utils import embedding_functions
default_ef = embedding_functions.DefaultEmbeddingFunction()

chroma_client = chromadb.PersistentClient(path=str(vector_db_path))
# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
collection = chroma_client.get_or_create_collection(name="my_collection")

# switch `add` to `upsert` to avoid adding the same documents every time
collection.upsert(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges"
    ],
    ids=["id1", "id2"]
)

results = collection.query(
    query_texts=["This is a query document about pineapple"], # Chroma will embed this for you
    n_results=1 # how many results to return
)

print(results)
