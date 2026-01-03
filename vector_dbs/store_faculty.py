import chromadb

# Directory where the database will be stored
PERSIST_DIR = "chroma_db"
client = chromadb.PersistentClient(path=PERSIST_DIR)
collection = client.get_collection(name="Faculty-embedings")




def add_faculty_member(faculty_id, faculty_embedding, faculty_metadata: dict):
    """Insert faculty only if not already in DB."""

    try:
        existing = collection.get(ids=[faculty_id])
    except Exception:
        print("[ERROR] Failed to check existing faculty.")
        return False

    # If ID found in database → skip insert
    if existing and existing.get("ids") and len(existing["ids"][0]) > 0:
        print(f"[INFO] Faculty ID '{faculty_id}' already exists. Skipping insert.")
        return False

    try:
        collection.add(
            ids=[faculty_id],
            embeddings=[faculty_embedding],
            metadatas=[faculty_metadata]
        )
        print(f"[SUCCESS] Faculty '{faculty_id}' added successfully.")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to add faculty '{faculty_id}': {e}")
        return False


def retrieve_from_db(query_embedding):
    """Retrieve ALL faces with similarity >= 0.7"""
    flat_query_embdings=[arr for sublist in query_embedding for arr in sublist]
    try:
        # Query more results (e.g., top 10)
        results = collection.query(
            query_embeddings=[flat_query_embdings],
            n_results=10,
            include=["embeddings", "metadatas", "distances"]
        )
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        return None

    matched_faces = []

    if results.get("ids") and len(results["ids"][0]) > 0:
        print("indide")
        distances = results["distances"][0]
        ids = results["ids"][0]
        metadatas = results["metadatas"][0]
        
        for i in range(len(ids)):
            distance = distances[i]

            # Convert distance → similarity
            similarity = 1 / (1 + distance)
            print(similarity)
            if similarity >= 0.7:    # threshold
                matched_faces.append({
                    "id": ids[i],
                    "similarity": float(similarity),
                    "metadata": metadatas[i],
                    "Present":"Person is found"
                })
    
    # If no matches above threshold
    if len(matched_faces) == 0:
        return "No matching faces found above similarity threshold (0.7)."

    return matched_faces



def delete_faculty_member(faculty_id: str):
    """Delete faculty by ID with safe checks."""

    try:
        existing = collection.get(ids=[faculty_id])
    except Exception as e:
        print(f"[ERROR] Unable to check faculty ID: {e}")
        return False

    # Check safely
    if not existing or not existing.get("ids") or len(existing["ids"][0]) == 0:
        print(f"[INFO] Faculty ID '{faculty_id}' does not exist. Nothing to delete.")
        return False

    # Perform deletion
    try:
        collection.delete(ids=[faculty_id])
        print(f"[SUCCESS] Faculty ID '{faculty_id}' deleted successfully.")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to delete faculty '{faculty_id}': {e}")
        return False


def main():
    pass


if __name__ == "__main__":
    main()