# memory.py
import os
import uuid
import psycopg2
from typing import Dict, Any
from mem0 import Memory as Mem0Memory


# Global Mem0 config ---------------------
os.environ["OPENAI_API_KEY"] = "sk"

config = {
    "vector_store": {
        "provider": "supabase",
        "config": {
            "connection_string": "postgresql://postgres:your-super-secret-and-long-postgres-password@localhost:54322/postgres",
            "collection_name": "memories",
            "index_method": "hnsw",
            "index_measure": "cosine_distance"
        }
    },
    "llm": {
        "provider": "vllm",
        "config": {
            "model": "Qwen/Qewn2.5-7B-Instruct",
            "vllm_base_url": "http://localhost:30000/v1",
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "huggingface_base_url": "http://localhost:4444/v1"
        }
    }
}

# 

class Memory:
    def __init__(self, user_id: str, session_id: str, db_url: str):
        self.user_id = user_id
        self.db_url = db_url
        
        # initialize mem0
        self.mem0 = Mem0Memory.from_config(config)

        # session handling
        self.session_id = (
            session_id if session_id is not None else str(uuid.uuid4())
        )


    def start_new_session(self):
        """Start a new chat session."""
        self.session_id = str(uuid.uuid4())
        return self.session_id


    def add_memory(self, message: str, role: str = "user") -> bool:
        """Add a single turn to Mem0 + Postgres."""
        try:
            metadata = {
                "user_id": self.user_id,
                "session_id": self.session_id,
                "role": role
            }

            # store in mem0
            self.mem0.add(memory=message, metadata=metadata, user_id=self.user_id)

            # store in postgres
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO conversation_context (user_id, role, message)
                VALUES (%s, %s, %s)
                """,
                (self.user_id, role, message)
            )
            conn.commit()
            cur.close()
            conn.close()

            return True

        except Exception as e:
            print(f"[Memory Error] Adding memory: {e}")
            return False


    def retrieve_memory(self, query: str = "", mem0_limit: int = 50) -> Dict[str, Any]:
        """Retrieve relevant memories for the current user."""
        try:
            # Mem0 vector retrieval
            results = self.mem0.search(
                query=query,
                user_id=self.user_id,
                limit=mem0_limit,
            )

            memory_entries = [
                f"{r['metadata']['role']}: {r['memory']}"
                for r in results.get("results", [])
            ]

            # Retrieve entire conversation history
            conn = psycopg2.connect(self.db_url)
            cur = conn.cursor()
            cur.execute(
                """
                SELECT role, message FROM conversation_context
                WHERE user_id = %s
                ORDER BY id ASC
                """,
                (self.user_id,)
            )
            ctx_rows = cur.fetchall()
            cur.close()
            conn.close()

            conversation_ctx = "\n".join(f"{role}: {msg}" for role, msg in ctx_rows)

            return {
                "conversation_ctx": conversation_ctx,
                "retrieved_memories": memory_entries
            }

        except Exception as e:
            print(f"[Memory Error] Retrieving memory: {e}")
            return {"error": "retrieval failed"}


if __name__ == "__main__":

    test_instance = Memory(user_id="alice_test", session_id=None, db_url="postgresql://postgres:your-super-secret-and-long-postgres-password@localhost:54322/postgres")
    pass

