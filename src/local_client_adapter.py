import os
import json
import uuid
from typing import List, Dict, Any, Optional
import sys

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pageindex import page_index
from pageindex.core.llm import extract_json
import pageindex.utils as utils

class PageIndexClient:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self.documents = {} # doc_id -> {status, structure, path, ...}

    def submit_document(self, file_path: str) -> Dict[str, str]:
        doc_id = str(uuid.uuid4())
        self.documents[doc_id] = {
            "status": "processing",
            "file_path": file_path,
            "structure": None
        }
        
        # In a real app this would be async background work, 
        # but for notebook compatibility we can either block or just set it to run on next access.
        # Since notebooks check status, we can run it synchronously here or lazily.
        # Let's run synchronously for simplicity as page_index is blocking/async.
        
        # We need to run async page_index in a sync context if this method is sync.
        # But page_index_main uses asyncio.run() internally? 
        # Let's check page_index.py. 
        # page_index() calls ConfigLoader then page_index_main(doc, opt).
        # page_index_main returns asyncio.run(page_index_builder()) 
        # So it IS blocking and synchronous from caller perspective.
        
        try:
             result = page_index(file_path)
             self.documents[doc_id]["structure"] = result["structure"]
             self.documents[doc_id]["status"] = "completed"
             self.documents[doc_id]["info"] = {
                 "id": doc_id,
                 "name": os.path.basename(file_path),
                 "status": "completed",
                 "pageNum": 0, # We might need to count pages if not in result
                 "description": result.get("doc_description", "")
             }
        except Exception as e:
            self.documents[doc_id]["status"] = "failed"
            print(f"Error processing document: {e}")

        return {"doc_id": doc_id}

    def get_document(self, doc_id: str) -> Dict[str, Any]:
        doc = self.documents.get(doc_id)
        if not doc:
            return {"status": "not_found"}
        return doc.get("info", {"status": doc["status"]})

    def is_retrieval_ready(self, doc_id: str) -> bool:
        doc = self.documents.get(doc_id)
        return doc and doc["status"] == "completed"

    def get_tree(self, doc_id: str, node_summary: bool = False) -> Dict[str, Any]:
        doc = self.documents.get(doc_id)
        if not doc or not doc["structure"]:
            return {"result": []}
        return {"result": doc["structure"]}

    def chat_completions(self, messages: List[Dict[str, str]], doc_id: str, stream: bool = False):
        # This implementation mimics the RAG flow
        query = messages[-1]["content"]
        doc = self.documents.get(doc_id)
        if not doc or not doc["structure"]:
            yield "Data not found" if stream else "Data not found"
            return

        tree = doc["structure"]
        
        # 1. Search Tree (Async run in sync wrapper?)
        # Since this method is likely called synchronously in notebooks or awaited?
        # Notebooks usually use `pi_client.chat_completions` in a loop for stream.
        # If I can't await here, I have to handle async LLM calls.
        # But `pageindex.core.llm` has `ChatGPT_API` (sync) and `ChatGPT_API_async`.
        # I'll use the SYNC version `ChatGPT_API` for simplicity in this adapter.
        
        from pageindex.core.llm import ChatGPT_API
        
        # Remove text field for search to save tokens
        tree_without_text = utils.remove_fields(json.loads(json.dumps(tree)), fields=['text'])

        search_prompt = f"""
You are given a question and a tree structure of a document.
Each node contains a node id, node title, and a corresponding summary.
Your task is to find all nodes that are likely to contain the answer to the question.

Question: {query}

Document tree structure:
{json.dumps(tree_without_text, indent=2)}

Please reply in the following JSON format:
{{
    "thinking": "<Your thinking process>",
    "node_list": ["node_id_1", "node_id_2"]
}}
Directly return the final JSON structure.
"""
        tree_search_result = ChatGPT_API(model="gpt-4o", prompt=search_prompt)
        try:
            tree_search_json = extract_json(tree_search_result)
            node_ids = tree_search_json.get("node_list", [])
        except:
             node_ids = []

        # 2. Retrieve Context
        node_map = utils.create_node_mapping(tree)
        relevant_content = ""
        for nid in node_ids:
            if nid in node_map:
                relevant_content += node_map[nid].get("text", "") + "\n\n"

        # 3. Generate Answer
        answer_prompt = f"""
Answer the question based on the context:

Question: {query}
Context: {relevant_content[:20000]} 

Provide a clear, concise answer.
"""
        answer = ChatGPT_API(model="gpt-4o", prompt=answer_prompt)
        
        # Simulate stream by yielding chunks (or just one chunk)
        if stream:
            yield answer
        else:
            return answer

# Helper for notebooks to import
def get_client(api_key=None):
    return PageIndexClient(api_key=api_key)
