import json
import glob
import os

def refactor_notebook(path):
    print(f"Refactoring {path}...")
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. Inject Imports Cell
    # Check if we already injected it
    first_code_cell_idx = -1
    for i, cell in enumerate(nb['cells']):
        if cell['cell_type'] == 'code':
            first_code_cell_idx = i
            break
            
    if first_code_cell_idx != -1:
        # Check source content
        source = "".join(nb['cells'][first_code_cell_idx]['source'])
        if "local_client_adapter" not in source:
             # Create new cell or prepend to first cell?
             # Better to prepend to first code cell source if it's imports
             # Or insert new cell before it.
             new_source = [
                 "import sys\n",
                 "import os\n",
                 "sys.path.append(os.path.abspath('../src'))\n",
                 "from local_client_adapter import get_client\n",
                 "\n"
             ]
             # nb['cells'].insert(first_code_cell_idx, {
             #     'cell_type': 'code',
             #     'execution_count': None,
             #     'metadata': {},
             #     'outputs': [],
             #     'source': new_source
             # })
             # Actually safer to append to the start of the existing imports cell if strictly needed,
             # but inserting a new cell is cleaner.
             nb['cells'].insert(first_code_cell_idx, {
                 'cell_type': 'code',
                 'execution_count': None,
                 'metadata': {},
                 'outputs': [],
                 'source': new_source
             })

    # 2. Key replacements in all code cells
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            new_source = []
            for line in cell['source']:
                # Replace imports
                if "from pageindex import PageIndexClient" in line:
                    line = line.replace("from pageindex import PageIndexClient", "# from pageindex import PageIndexClient")
                
                # Replace client init
                if "PageIndexClient(" in line:
                    line = line.replace("PageIndexClient(", "get_client(")
                
                # Fix JsonExtractor if present
                if "from json_extractor import JsonExtractor" in line:
                    line = "# from json_extractor import JsonExtractor\nfrom pageindex.core.llm import extract_json, get_json_content\n"
                
                if "JsonExtractor.extract_valid_json" in line:
                    line = line.replace("JsonExtractor.extract_valid_json", "extract_json")
                
                # Comment out pip installs
                if "%pip install" in line:
                    line = "# " + line

                new_source.append(line)
            cell['source'] = new_source

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print(f"Saved {path}")

if __name__ == "__main__":
    files = glob.glob("../notebooks/*.ipynb")
    for f in files:
        if "pageindex_RAG_simple" in f:
            # Skip this one or handle differently?
            # It has no PageIndexClient import in my analysis? 
            # Wait, Cell 9 has: from pageindex import PageIndexClient
            # So it DOES use it. It should be refactored too.
            pass
        refactor_notebook(f)
