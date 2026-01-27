import sys
import os
sys.path.append(os.path.abspath('.'))
from local_client_adapter import get_client

def test_adapter():
    print("Testing Local Adapter...")
    client = get_client(api_key="TEST")
    print("Client initialized.")
    
    # Check methods exist
    assert hasattr(client, 'submit_document')
    assert hasattr(client, 'get_tree')
    assert hasattr(client, 'chat_completions')
    print("Methods verified.")

    # We can't easily test submit_document without a real file and openai key (which might be missing or mocking needed)
    # But we can verify imports are working.
    print("Imports and class structure verified.")

if __name__ == "__main__":
    test_adapter()
