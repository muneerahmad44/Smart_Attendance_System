import chromadb
def create_collection():
    PERSIST_DIR = "chroma_db"
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    
    try:
        client.create_collection(
            name="Faculty-embedings",
            metadata={'description': "Faculty member faces vector embeddings"}
        )
        print("[SUCCESS] Collection created.")
    except Exception as e:
        print("[INFO] Collection already exists. Skipping creation.")


create_collection()